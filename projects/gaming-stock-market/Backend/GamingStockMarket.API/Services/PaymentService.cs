using GamingStockMarket.API.DTOs;
using GamingStockMarket.API.Repositories;
using Microsoft.Extensions.Logging;
using Stripe;
using System;
using System.Threading.Tasks;
using System.Collections.Generic;
using GamingStockMarket.API.Services.Interfaces; // Added for IPaymentService
using Microsoft.Extensions.Configuration;

namespace GamingStockMarket.API.Services
{
    public class PaymentService : IPaymentService
    {
        private readonly ITransactionRepository _transactionRepository;
        private readonly IUserRepository _userRepository;
        private readonly ILogger<PaymentService> _logger;
        private readonly string _stripeSecretKey; // Added for Stripe Secret Key
        private readonly string _stripeWebhookSecret; // Added for Stripe Webhook Secret
        private readonly IAchievementService _achievementService; // Added for IAchievementService

        public PaymentService(ITransactionRepository transactionRepository, IUserRepository userRepository, 
                              ILogger<PaymentService> logger, IConfiguration configuration,
                              IAchievementService achievementService) // Added IConfiguration and IAchievementService
        {
            _transactionRepository = transactionRepository;
            _userRepository = userRepository;
            _logger = logger;
            _stripeSecretKey = configuration["StripeSettings:SecretKey"] ?? throw new ArgumentNullException("StripeSettings:SecretKey not found in configuration."); // Get from configuration
            _stripeWebhookSecret = configuration["StripeSettings:WebhookSecret"] ?? throw new ArgumentNullException("StripeSettings:WebhookSecret not found in configuration."); // Get from configuration
            _achievementService = achievementService; // Initialize IAchievementService

            // Set Stripe API key
            StripeConfiguration.ApiKey = _stripeSecretKey; 
        }

        public async Task<Models.Transaction> CreateDepositAsync(int userId, decimal amount, string currency, string paymentMethodId)
        {
            var user = await _userRepository.GetByIdAsync(userId);
            if (user == null) throw new Exception("User not found.");

            var transaction = new Models.Transaction
            {
                UserId = userId,
                Type = Models.TransactionType.Deposit,
                Amount = amount,
                Status = "PENDING",
                CreatedAt = DateTime.UtcNow,
                ExternalTransactionId = Guid.NewGuid().ToString() // Placeholder for Stripe charge ID
            };
            await _transactionRepository.AddAsync(transaction);

            try
            {
                var options = new PaymentIntentCreateOptions
                {
                    Amount = (long)(amount * 100), // Stripe expects amount in cents
                    Currency = currency.ToLower(),
                    PaymentMethod = paymentMethodId,
                    Confirm = true,
                    OffSession = true, // To charge customer without them being present
                    Customer = user.StripeCustomerId ?? await CreateStripeCustomer(user), // Assuming StripeCustomerId on User model
                    Description = $"Deposit for user {userId}"
                };
                var service = new PaymentIntentService();
                var paymentIntent = await service.CreateAsync(options);

                if (paymentIntent.Status == "succeeded")
                {
                    transaction.Status = "COMPLETED";
                    transaction.CompletedAt = DateTime.UtcNow;
                    user.Balance += amount;
                    await _userRepository.UpdateAsync(user);
                    _logger.LogInformation($"Deposit of {amount} {currency} completed for user {userId}.");

                    // Check for achievements after a successful deposit
                    await _achievementService.CheckAndGrantAchievementsAsync(userId);
                }
                else
                {
                    transaction.Status = "FAILED";
                    _logger.LogWarning($"Deposit of {amount} {currency} failed for user {userId}. Status: {paymentIntent.Status}");
                }
            }
            catch (StripeException ex)
            {
                transaction.Status = "FAILED";
                _logger.LogError(ex, "Stripe error during deposit for user {UserId}.", userId);
                throw;
            }
            finally
            {
                await _transactionRepository.UpdateAsync(transaction);
            }

            return transaction;
        }

        public async Task<Models.Transaction> CreateWithdrawalAsync(int userId, decimal amount, string currency, string withdrawalMethodDetails)
        {
            var user = await _userRepository.GetByIdAsync(userId);
            if (user == null) throw new Exception("User not found.");
            if (user.Balance < amount) throw new Exception("Insufficient balance for withdrawal.");
            // TODO: Add KYC verification check for withdrawal

            var transaction = new Models.Transaction
            {
                UserId = userId,
                Type = Models.TransactionType.Withdrawal,
                Amount = amount,
                Status = "PENDING", // Pending manual review or external processing
                CreatedAt = DateTime.UtcNow,
                Notes = $"Withdrawal to {withdrawalMethodDetails}"
            };
            await _transactionRepository.AddAsync(transaction);

            // For simplicity, directly deduct balance for now. In real-world, this would involve
            // integration with a payment gateway for payouts and a more robust status workflow.
            user.Balance -= amount;
            await _userRepository.UpdateAsync(user);

            transaction.Status = "COMPLETED"; // Assuming immediate completion for now
            transaction.CompletedAt = DateTime.UtcNow;
            await _transactionRepository.UpdateAsync(transaction);

            _logger.LogInformation($"Withdrawal of {amount} {currency} created for user {userId}.");

            return transaction;
        }

        public async Task HandleStripeWebhookAsync(string json, string stripeSignature, string webhookSecret)
        {
            // var webhookSecret = "whsec_YOUR_WEBHOOK_SECRET"; // TODO: Get from configuration

            try
            {
                var stripeEvent = EventUtility.ConstructEvent(json, stripeSignature, webhookSecret);

                if (stripeEvent.Type == Events.PaymentIntentSucceeded)
                {
                    var paymentIntent = stripeEvent.Data.Object as PaymentIntent;
                    _logger.LogInformation($"Stripe Webhook: PaymentIntent succeeded for ID: {paymentIntent?.Id}");

                    // Find corresponding transaction and update status
                    // var transaction = await _transactionRepository.GetByExternalTransactionIdAsync(paymentIntent.Id);
                    // if (transaction != null) { /* update transaction, user balance */ }
                }
                // Handle other event types like payment_intent.payment_failed, charge.refunded, etc.
            }
            catch (StripeException ex)
            {
                _logger.LogError(ex, "Stripe Webhook Error: {Message}", ex.Message);
                throw;
            }
        }

        private async Task<string> CreateStripeCustomer(Models.User user)
        {
            var customerOptions = new CustomerCreateOptions
            {
                Email = user.Email,
                Name = user.Username,
                Metadata = new Dictionary<string, string> { { "userId", user.Id.ToString() } }
            };
            var customerService = new CustomerService();
            var customer = await customerService.CreateAsync(customerOptions);

            // Update user with StripeCustomerId
            user.StripeCustomerId = customer.Id; // Assuming StripeCustomerId property in User model
            await _userRepository.UpdateAsync(user);

            return customer.Id;
        }
    }
}

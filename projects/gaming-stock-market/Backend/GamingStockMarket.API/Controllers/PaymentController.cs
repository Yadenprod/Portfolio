using Microsoft.AspNetCore.Mvc;
using GamingStockMarket.API.DTOs;
using GamingStockMarket.API.Extensions;
using Microsoft.AspNetCore.Authorization;
using Microsoft.Extensions.Logging;
using Stripe;
using System;
using System.Threading.Tasks;
using GamingStockMarket.API.Services.Interfaces; // Added for IPaymentService

namespace GamingStockMarket.API.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    [Authorize]
    public class PaymentController : ControllerBase
    {
        private readonly IPaymentService _paymentService;
        private readonly ILogger<PaymentController> _logger;

        public PaymentController(IPaymentService paymentService, ILogger<PaymentController> logger)
        {
            _paymentService = paymentService;
            _logger = logger;
        }

        [HttpPost("deposit")]
        public async Task<ActionResult<PaymentResponse>> Deposit([FromBody] DepositRequest request)
        {
            try
            {
                var userId = User.GetUserId();
                var transaction = await _paymentService.CreateDepositAsync(userId, request.Amount, request.Currency, request.PaymentMethodId);
                
                _logger.LogInformation($"Deposit initiated for user {userId}: {request.Amount} {request.Currency}.");

                return Ok(new PaymentResponse
                {
                    TransactionId = transaction.Id,
                    Status = transaction.Status,
                    Amount = transaction.Amount,
                    Currency = request.Currency
                });
            }
            catch (StripeException ex)
            {
                _logger.LogError(ex, "Stripe payment error during deposit for user {UserId}.", User.GetUserId());
                return BadRequest(new { message = ex.Message });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error during deposit for user {UserId}.", User.GetUserId());
                return StatusCode(500, new { message = "Internal server error." });
            }
        }

        [HttpPost("withdraw")]
        public async Task<ActionResult<PaymentResponse>> Withdraw([FromBody] WithdrawalRequest request)
        {
            try
            {
                var userId = User.GetUserId();
                var transaction = await _paymentService.CreateWithdrawalAsync(userId, request.Amount, request.Currency, request.WithdrawalMethodDetails);

                _logger.LogInformation($"Withdrawal initiated for user {userId}: {request.Amount} {request.Currency}.");

                return Ok(new PaymentResponse
                {
                    TransactionId = transaction.Id,
                    Status = transaction.Status,
                    Amount = transaction.Amount,
                    Currency = request.Currency
                });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error during withdrawal for user {UserId}.", User.GetUserId());
                return BadRequest(new { message = ex.Message });
            }
        }
    }
}

using Microsoft.Extensions.Logging;
using System.Threading.Tasks;
using GamingStockMarket.API.Services.Interfaces; // Added for IEmailService

namespace GamingStockMarket.API.Services
{
    public class EmailService : IEmailService
    {
        private readonly ILogger<EmailService> _logger;

        public EmailService(ILogger<EmailService> logger)
        {
            _logger = logger;
        }

        public Task SendEmailAsync(string to, string subject, string body)
        {
            // This is a dummy implementation. In a real application, you would integrate with SendGrid, Mailgun, etc.
            _logger.LogInformation($"Sending email to {to} with subject \"{subject}\" and body: \"{body}\"");
            return Task.CompletedTask;
        }
    }
}

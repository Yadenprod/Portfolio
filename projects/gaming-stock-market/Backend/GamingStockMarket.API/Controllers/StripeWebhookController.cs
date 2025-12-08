using Microsoft.Extensions.Configuration;
using Microsoft.AspNetCore.Mvc;
using GamingStockMarket.API.Services.Interfaces;
using Microsoft.Extensions.Logging;
using Stripe;
using System.IO;
using System.Threading.Tasks;

namespace GamingStockMarket.API.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class StripeWebhookController : ControllerBase
    {
        private readonly IPaymentService _paymentService;
        private readonly ILogger<StripeWebhookController> _logger;
        private readonly IConfiguration _configuration; // Add IConfiguration

        public StripeWebhookController(IPaymentService paymentService, ILogger<StripeWebhookController> logger, IConfiguration configuration)
        {
            _paymentService = paymentService;
            _logger = logger;
            _configuration = configuration; // Initialize IConfiguration
        }

        [HttpPost]
        public async Task<IActionResult> HandleWebhook()
        {
            var json = await new StreamReader(HttpContext.Request.Body).ReadToEndAsync();
            var stripeSignature = Request.Headers["Stripe-Signature"];
            var webhookSecret = _configuration["StripeSettings:WebhookSecret"]; // Get webhook secret from config

            try
            {
                await _paymentService.HandleStripeWebhookAsync(json, stripeSignature, webhookSecret);
                return Ok();
            }
            catch (StripeException ex)
            {
                _logger.LogError(ex, "Stripe Webhook Error: {Message}", ex.Message);
                return BadRequest();
            }
            catch (System.Exception ex)
            {
                _logger.LogError(ex, "General Webhook Error: {Message}", ex.Message);
                return StatusCode(500); 
            }
        }
    }
}

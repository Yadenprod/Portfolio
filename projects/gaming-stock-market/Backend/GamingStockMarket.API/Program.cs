using Microsoft.AspNetCore.Builder;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using GamingStockMarket.API.Data;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using GamingStockMarket.API.Repositories;
using GamingStockMarket.API.Services;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.IdentityModel.Tokens;
using System.Text;
using GamingStockMarket.API.BackgroundServices;
using GamingStockMarket.API.Services.Interfaces;
using Microsoft.AspNetCore.RateLimiting;
using System.Threading.RateLimiting;
using System.Security.Claims;
using GamingStockMarket.API.Hubs;
using Stripe; // Added for Stripe configuration
using Serilog; // Added for Serilog
using GamingStockMarket.API.Models;
using GamingStockMarket.API.Configuration;
using Microsoft.AspNetCore.Diagnostics.HealthChecks; // Added for HealthChecks
using HealthChecks.UI.Client; // Added for HealthChecks UI

var builder = WebApplication.CreateBuilder(args);

// Configure Serilog
Log.Logger = new LoggerConfiguration()
    .ReadFrom.Configuration(builder.Configuration)
    .Enrich.FromLogContext()
    .WriteTo.Console()
    .CreateLogger();

builder.Host.UseSerilog(); // Integrate Serilog with the host

// Add services to the container.
builder.Services.AddControllers();
// Learn more about configuring Swagger/OpenAPI at https://aka.ms/aspnetcore/swashbuckle
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

// Configure PostgreSQL
builder.Services.AddDbContext<ApplicationDbContext>(options =>
    options.UseNpgsql(builder.Configuration.GetConnectionString("DefaultConnection"))
);

// Add Repositories
builder.Services.AddScoped<IUserRepository, UserRepository>();
builder.Services.AddScoped<IPlayerRepository, PlayerRepository>();
builder.Services.AddScoped<ITeamRepository, TeamRepository>();
builder.Services.AddScoped<IOrderRepository, OrderRepository>();
builder.Services.AddScoped<ITradeRepository, TradeRepository>();
builder.Services.AddScoped<IUserPortfolioRepository, UserPortfolioRepository>();
builder.Services.AddScoped<IMatchRepository, MatchRepository>();
builder.Services.AddScoped<IPriceHistoryRepository, PriceHistoryRepository>();
builder.Services.AddScoped<ITransactionRepository, TransactionRepository>();
builder.Services.AddScoped<IAchievementRepository, AchievementRepository>();
builder.Services.AddScoped<INotificationRepository, NotificationRepository>();
builder.Services.AddScoped<IAuditLogRepository, AuditLogRepository>();

// Add Services
builder.Services.AddScoped<IUserService, UserService>();
builder.Services.AddScoped<IJwtService, JwtService>();
builder.Services.AddScoped<IPaymentService, PaymentService>();
builder.Services.AddScoped<IAnalyticsService, AnalyticsService>();
builder.Services.AddScoped<IAchievementService, AchievementService>();
builder.Services.AddScoped<IDataParser, CSGOParser>(); // Register CSGOParser as IDataParser
builder.Services.AddScoped<IPriceCalculator, PriceCalculator>();
builder.Services.AddScoped<ITradingService, TradingService>();
builder.Services.AddScoped<IEmailService, EmailService>(); // Added EmailService
builder.Services.AddScoped<IKycService, KycService>(); // Added KycService
builder.Services.AddScoped<ITwoFactorAuthService, TwoFactorAuthService>(); // Added TwoFactorAuthService
builder.Services.AddScoped<INotificationService, GamingStockMarket.API.Services.NotificationService>();
builder.Services.AddHostedService<GamingStockMarket.API.BackgroundServices.NotificationService>();

// Configure Stripe (using options pattern)
builder.Services.Configure<StripeSettings>(builder.Configuration.GetSection("StripeSettings"));
StripeConfiguration.ApiKey = builder.Configuration["StripeSettings:SecretKey"];

// Configure Email Service (using options pattern)
builder.Services.Configure<EmailServiceSettings>(builder.Configuration.GetSection("EmailServiceSettings"));

// Add singleton OrderBook for in-memory order matching
builder.Services.AddSingleton<OrderBook>();

// Add HttpClient for data parsing
builder.Services.AddHttpClient<CSGOParser>();

// Add Background Services
builder.Services.AddHostedService<PriceUpdateService>();
builder.Services.AddHostedService<DataParsingService>();
builder.Services.AddHostedService<MarketMakerService>();
builder.Services.AddHostedService<NotificationService>();
builder.Services.AddHostedService<AuditService>();

// Add JWT Authentication
builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options =>
    {
        options.TokenValidationParameters = new TokenValidationParameters
        {
            ValidateIssuer = true,
            ValidateAudience = true,
            ValidateLifetime = true,
            ValidateIssuerSigningKey = true,
            ValidIssuer = builder.Configuration["JwtSettings:Issuer"],
            ValidAudience = builder.Configuration["JwtSettings:Audience"],
            IssuerSigningKey = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(builder.Configuration["JwtSettings:SecretKey"]))
        };
    });

builder.Services.AddAuthorization();

// Configure CORS
builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowSpecificOrigin",
        builder => builder.WithOrigins("http://localhost:3000") // React app URL
                            .AllowAnyHeader()
                            .AllowAnyMethod()
                            .AllowCredentials());
});

// Add SignalR
builder.Services.AddSignalR(options =>
{
    options.EnableDetailedErrors = true;
    // options.AddHubOptions<TradingHub>(hubOptions =>
    // {
    //     hubOptions.EnableDetailedErrors = true;
    // });
});

// Add Response Caching
builder.Services.AddResponseCaching();

// Add Health Checks
builder.Services.AddHealthChecks()
    .AddNpgSql(builder.Configuration.GetConnectionString("DefaultConnection")!, name: "PostgreSQL-DB-Check", tags: new[] { "db", "ready" });

// Configure Rate Limiting
builder.Services.AddRateLimiter(options =>
{
    options.AddFixedWindowLimiter("fixed", fixedWindowOptions =>
    {
        fixedWindowOptions.PermitLimit = 10;
        fixedWindowOptions.Window = TimeSpan.FromSeconds(10);
        fixedWindowOptions.QueueProcessingOrder = QueueProcessingOrder.OldestFirst;
        fixedWindowOptions.QueueLimit = 5;
    });

    options.RejectionStatusCode = StatusCodes.Status429TooManyRequests;
});

var app = builder.Build();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();

// Use Response Caching (must be before UseRouting)
app.UseResponseCaching();

// Add security headers
app.Use(async (context, next) =>
{
    context.Response.Headers.Add("X-Content-Type-Options", "nosniff");
    context.Response.Headers.Add("X-Frame-Options", "DENY");
    context.Response.Headers.Add("Referrer-Policy", "no-referrer");
    context.Response.Headers.Add("X-XSS-Protection", "1; mode=block");
    context.Response.Headers.Add("Strict-Transport-Security", "max-age=31536000; includeSubDomains");
    await next();
});

app.UseCors("AllowSpecificOrigin"); // Use CORS policy

app.UseRateLimiter(); // Use Rate Limiting

app.UseAuthentication(); // Must be before UseAuthorization
app.UseAuthorization();

// Map Health Checks
app.MapHealthChecks("/health/ready", new Microsoft.AspNetCore.Diagnostics.HealthChecks.HealthCheckOptions
{
    Predicate = (check) => check.Tags.Contains("ready"),
    ResponseWriter = UIResponseWriter.WriteHealthCheckUIResponse // Changed to UIResponseWriter
});
app.MapHealthChecks("/health/live", new Microsoft.AspNetCore.Diagnostics.HealthChecks.HealthCheckOptions
{
    Predicate = (_) => false,
    ResponseWriter = UIResponseWriter.WriteHealthCheckUIResponse // Changed to UIResponseWriter
});

// Map SignalR Hubs
app.MapHub<TradingHub>("/hubs/trading");
app.MapHub<NotificationHub>("/hubs/notification");

app.MapControllers();

app.Run();

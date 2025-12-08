using Microsoft.EntityFrameworkCore;
using GamingStockMarket.API.Models;
using Microsoft.EntityFrameworkCore.Metadata;

namespace GamingStockMarket.API.Data
{
    public class ApplicationDbContext : DbContext
    {
        public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options) : base(options)
        {
        }

        public DbSet<User> Users { get; set; }
        public DbSet<Player> Players { get; set; }
        public DbSet<Team> Teams { get; set; }
        public DbSet<Order> Orders { get; set; }
        public DbSet<Trade> Trades { get; set; }
        public DbSet<UserPortfolio> UserPortfolios { get; set; }
        public DbSet<Match> Matches { get; set; }
        public DbSet<PriceHistory> PriceHistory { get; set; }
        public DbSet<Transaction> Transactions { get; set; }
        public DbSet<Achievement> Achievements { get; set; }
        public DbSet<Notification> Notifications { get; set; }
        public DbSet<AuditLog> AuditLogs { get; set; }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);

            // User - Order (One-to-Many)
            modelBuilder.Entity<Order>()
                .HasOne(o => o.User)
                .WithMany(u => u.Orders)
                .HasForeignKey(o => o.UserId)
                .IsRequired(false) // Make foreign key optional
                .OnDelete(DeleteBehavior.SetNull); // Set UserId to null if User is deleted

            // User - UserPortfolio (One-to-Many)
            modelBuilder.Entity<UserPortfolio>()
                .HasOne(up => up.User)
                .WithMany(u => u.Portfolio)
                .HasForeignKey(up => up.UserId)
                .IsRequired(false) // Make foreign key optional
                .OnDelete(DeleteBehavior.SetNull); // Set UserId to null if User is deleted

            // User - Transaction (One-to-Many)
            modelBuilder.Entity<Transaction>()
                .HasOne(t => t.User)
                .WithMany(u => u.Transactions)
                .HasForeignKey(t => t.UserId)
                .IsRequired(false) // Make foreign key optional
                .OnDelete(DeleteBehavior.SetNull); // Set UserId to null if User is deleted

            // User - Notification (One-to-Many)
            modelBuilder.Entity<Notification>()
                .HasOne(n => n.User)
                .WithMany(u => u.Notifications)
                .HasForeignKey(n => n.UserId)
                .IsRequired(false) // Make foreign key optional
                .OnDelete(DeleteBehavior.SetNull); // Set UserId to null if User is deleted

            // User - AuditLog (One-to-Many)
            modelBuilder.Entity<AuditLog>()
                .HasOne(al => al.User)
                .WithMany(u => u.AuditLogs)
                .HasForeignKey(al => al.UserId)
                .IsRequired(false) // Make foreign key optional
                .OnDelete(DeleteBehavior.SetNull); // Set UserId to null if User is deleted

            // User - Achievement (One-to-Many)
            modelBuilder.Entity<Achievement>()
                .HasOne(a => a.User)
                .WithMany(u => u.Achievements)
                .HasForeignKey(a => a.UserId)
                .IsRequired(false) // Make foreign key optional
                .OnDelete(DeleteBehavior.SetNull); // Set UserId to null if User is deleted

            // Player - Order (One-to-Many, optional)
            modelBuilder.Entity<Order>()
                .HasOne(o => o.Player)
                .WithMany(p => p.Orders)
                .HasForeignKey(o => o.PlayerId)
                .IsRequired(false) // PlayerId can be null for team orders
                .OnDelete(DeleteBehavior.Restrict);

            // Player - Trade (One-to-Many, optional)
            modelBuilder.Entity<Trade>()
                .HasOne(t => t.Player)
                .WithMany(p => p.Trades)
                .HasForeignKey(t => t.PlayerId)
                .IsRequired(false)
                .OnDelete(DeleteBehavior.Restrict);

            // Player - UserPortfolio (One-to-Many, optional)
            modelBuilder.Entity<UserPortfolio>()
                .HasOne(up => up.Player)
                .WithMany(p => p.PortfolioHoldings)
                .HasForeignKey(up => up.PlayerId)
                .IsRequired(false)
                .OnDelete(DeleteBehavior.Restrict);

            // Player - Match (One-to-Many, optional)
            modelBuilder.Entity<Match>()
                .HasOne(m => m.Player)
                .WithMany(p => p.Matches)
                .HasForeignKey(m => m.PlayerId)
                .IsRequired(false)
                .OnDelete(DeleteBehavior.Restrict);

            // Player - PriceHistory (One-to-Many, optional)
            modelBuilder.Entity<PriceHistory>()
                .HasOne(ph => ph.Player)
                .WithMany(p => p.PriceHistory)
                .HasForeignKey(ph => ph.PlayerId)
                .IsRequired(false)
                .OnDelete(DeleteBehavior.Restrict);

            // Team - Order (One-to-Many, optional)
            modelBuilder.Entity<Order>()
                .HasOne(o => o.Team)
                .WithMany(t => t.Orders)
                .HasForeignKey(o => o.TeamId)
                .IsRequired(false) // TeamId can be null for player orders
                .OnDelete(DeleteBehavior.Restrict);

            // Team - Trade (One-to-Many, optional)
            modelBuilder.Entity<Trade>()
                .HasOne(t => t.Team)
                .WithMany(tm => tm.Trades)
                .HasForeignKey(t => t.TeamId)
                .IsRequired(false)
                .OnDelete(DeleteBehavior.Restrict);

            // Team - UserPortfolio (One-to-Many, optional)
            modelBuilder.Entity<UserPortfolio>()
                .HasOne(up => up.Team)
                .WithMany(tm => tm.PortfolioHoldings)
                .HasForeignKey(up => up.TeamId)
                .IsRequired(false)
                .OnDelete(DeleteBehavior.Restrict);

            // Team - Match (One-to-Many, optional)
            modelBuilder.Entity<Match>()
                .HasOne(m => m.Team)
                .WithMany(t => t.Matches)
                .HasForeignKey(m => m.TeamId)
                .IsRequired(false)
                .OnDelete(DeleteBehavior.Restrict);

            // Team - PriceHistory (One-to-Many, optional)
            modelBuilder.Entity<PriceHistory>()
                .HasOne(ph => ph.Team)
                .WithMany(t => t.PriceHistory)
                .HasForeignKey(ph => ph.TeamId)
                .IsRequired(false)
                .OnDelete(DeleteBehavior.Restrict);

            // Trade - Order (One-to-One, optional for buy/sell side)
            modelBuilder.Entity<Trade>()
                .HasOne(t => t.BuyOrder)
                .WithMany(o => o.BuyTrades)
                .HasForeignKey(t => t.BuyOrderId)
                .OnDelete(DeleteBehavior.Restrict);

            modelBuilder.Entity<Trade>()
                .HasOne(t => t.SellOrder)
                .WithMany(o => o.SellTrades)
                .HasForeignKey(t => t.SellOrderId)
                .OnDelete(DeleteBehavior.Restrict);

            // Unique constraints and indexes
            modelBuilder.Entity<User>().HasIndex(u => u.Username).IsUnique();
            modelBuilder.Entity<User>().HasIndex(u => u.Email).IsUnique();
            modelBuilder.Entity<Player>().HasIndex(p => new { p.Name, p.Game }).IsUnique();
            modelBuilder.Entity<Team>().HasIndex(t => new { t.Name, t.Game }).IsUnique();
            modelBuilder.Entity<UserPortfolio>().HasIndex(up => new { up.UserId, up.PlayerId, up.TeamId }).IsUnique();

            // Global query filters for soft delete
            modelBuilder.Entity<User>().HasQueryFilter(u => u.IsActive);
            modelBuilder.Entity<Player>().HasQueryFilter(p => p.IsActive);
            modelBuilder.Entity<Team>().HasQueryFilter(t => t.IsActive);

            // Audit properties
            foreach (var entityType in modelBuilder.Model.GetEntityTypes())
            {
                var createdAtProperty = entityType.FindProperty("CreatedAt");
                if (createdAtProperty != null && createdAtProperty.ValueGenerated == ValueGenerated.Never)
                {
                    createdAtProperty.SetDefaultValueSql("CURRENT_TIMESTAMP");
                }

                var updatedAtProperty = entityType.FindProperty("UpdatedAt");
                if (updatedAtProperty != null && updatedAtProperty.ValueGenerated == ValueGenerated.Never)
                {
                    updatedAtProperty.SetDefaultValueSql("CURRENT_TIMESTAMP");
                    updatedAtProperty.SetBeforeSaveBehavior(PropertySaveBehavior.Save);
                }
            }
        }

        public override int SaveChanges()
        {
            AddAuditInfo();
            return base.SaveChanges();
        }

        public override Task<int> SaveChangesAsync(CancellationToken cancellationToken = new CancellationToken())
        {
            AddAuditInfo();
            return base.SaveChangesAsync(cancellationToken);
        }

        private void AddAuditInfo()
        {
            var entries = ChangeTracker.Entries()
                .Where(x => x.Entity is BaseModel && (x.State == EntityState.Added || x.State == EntityState.Modified));

            foreach (var entry in entries)
            {
                if (entry.State == EntityState.Added)
                {
                    ((BaseModel)entry.Entity).CreatedAt = DateTime.UtcNow;
                }
                ((BaseModel)entry.Entity).UpdatedAt = DateTime.UtcNow;
            }
        }
    }
}

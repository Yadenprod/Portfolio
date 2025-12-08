namespace GamingStockMarket.API.Services.Interfaces
{
    public interface IDataParser
    {
        Task UpdatePlayerDataAsync();
        Task UpdateMatchesAsync();
        Task UpdateTeamDataAsync();
    }
}

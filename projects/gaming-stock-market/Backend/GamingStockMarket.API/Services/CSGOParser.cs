using GamingStockMarket.API.Models;
using GamingStockMarket.API.Repositories;
using Microsoft.Extensions.Logging;
using System.Net.Http;
using System.Text.RegularExpressions;
using System.Threading.Tasks;
using System.Collections.Generic;
using System.Linq;
using System;
using GamingStockMarket.API.Services.Interfaces; // Added for IDataParser

namespace GamingStockMarket.API.Services
{
    public class CSGOParser : IDataParser
    {
        private readonly HttpClient _httpClient;
        private readonly ILogger<CSGOParser> _logger;
        private readonly IPlayerRepository _playerRepository;
        private readonly IMatchRepository _matchRepository;
        private readonly ITeamRepository _teamRepository;

        public CSGOParser(HttpClient httpClient, ILogger<CSGOParser> logger,
                          IPlayerRepository playerRepository, IMatchRepository matchRepository, ITeamRepository teamRepository)
        {
            _httpClient = httpClient;
            _logger = logger;
            _playerRepository = playerRepository;
            _matchRepository = matchRepository;
            _teamRepository = teamRepository;
        }

        public async Task UpdatePlayerDataAsync()
        {
            _logger.LogInformation("Starting CS:GO player data update...");
            try
            {
                var players = await _playerRepository.GetActivePlayersByGameAsync("CS:GO");
                
                foreach (var player in players)
                {
                    await UpdatePlayerStats(player);
                    await Task.Delay(1000); // Rate limiting for external API calls
                }
                _logger.LogInformation("CS:GO player data update completed.");
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error updating CS:GO player data");
            }
        }

        public async Task UpdateMatchesAsync()
        {
            _logger.LogInformation("Starting CS:GO match data update...");
            try
            {
                /*
                var matchesUrl = "https://www.hltv.org/matches"; // Simplified URL
                var html = await GetHtmlWithRetry(matchesUrl);
                
                if (!string.IsNullOrEmpty(html))
                {
                    var matches = ParseMatchesFromHtml(html, "CS:GO");
                    foreach (var match in matches)
                    {
                        var existingMatch = await _matchRepository.GetRecentMatchesAsync(match.PlayerId, match.TeamId, 1)
                                                                .ContinueWith(t => t.Result.FirstOrDefault(m => m.MatchDate == match.MatchDate && m.Tournament == match.Tournament));

                        if (existingMatch == null)
                        {
                            await _matchRepository.AddAsync(match);
                        }
                    }
                    _logger.LogInformation($"Updated {matches.Count} CS:GO matches.");
                }
                */
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error updating CS:GO matches");
            }
        }

        public async Task UpdateTeamDataAsync()
        {
            _logger.LogInformation("Starting CS:GO team data update...");
            try
            {
                var teams = await _teamRepository.GetActiveTeamsByGameAsync("CS:GO");

                foreach (var team in teams)
                {
                    // Simplified: In a real scenario, this would involve parsing team-specific data
                    // from a source like HLTV or Liquipedia to update ranking, etc.
                    // For now, we'll just log it.
                    _logger.LogInformation($"Simulating team data update for {team.Name}.");
                    await Task.Delay(500); // Simulate work
                }
                _logger.LogInformation("CS:GO team data update completed.");
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error updating CS:GO team data");
            }
        }

        private async Task UpdatePlayerStats(Player player)
        {
            try
            {
                /*
                var statsUrl = $"https://www.hltv.org/stats/players/{player.Id}/{player.Name.Replace(" ", "-").ToLower()}";
                var html = await GetHtmlWithRetry(statsUrl);
                
                if (!string.IsNullOrEmpty(html))
                {
                    var rating = ExtractRatingFromHtml(html); // Implement actual parsing
                    player.Rating = rating;
                    await _playerRepository.UpdateAsync(player);
                    _logger.LogInformation($"Updated stats for {player.Name}: Rating {rating}");
                }
                */
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error updating stats for {player.Name}");
            }
        }

        /*
        private decimal? ExtractRatingFromHtml(string html)
        {
            // Simplified parsing: Look for a pattern like "Rating 2.0" followed by a number
            var match = Regex.Match(html, @"Rating 2\.0.*?<span[^>]*?>([\d\.]+?)</span>", RegexOptions.Singleline);
            if (match.Success && decimal.TryParse(match.Groups[1].Value, out var rating))
            {
                return rating;
            }
            _logger.LogWarning("Could not extract rating from HTML.");
            return null;
        }

        private List<Match> ParseMatchesFromHtml(string html, string game)
        {
            var matches = new List<Match>();
            // This is a highly simplified example. Real parsing would need a robust HTML parser (e.g., AngleSharp).
            // Look for match containers and extract relevant data.
            var matchContainers = Regex.Matches(html, @"<div\s+class=\"match-item\"[^>]*?>([\s\S]*?)</div>", RegexOptions.Multiline);
            foreach (Match container in matchContainers)
            {
                // Example: Extract team names, result, tournament. Very fragile without a proper HTML parser.
                var team1Match = Regex.Match(container.Value, @"<div\s+class=\"team-left\"[^>]*?>.*?<div\s+class=\"team-name\"[^>]*?>(.*?)</div>", RegexOptions.Singleline);
                var team2Match = Regex.Match(container.Value, @"<div\s+class=\"team-right\"[^>]*?>.*?<div\s+class=\"team-name\"[^>]*?>(.*?)</div>", RegexOptions.Singleline);
                var resultMatch = Regex.Match(container.Value, @"<div\s+class=\"match-score\"[^>]*?>(.*?)</div>", RegexOptions.Singleline);
                var tournamentMatch = Regex.Match(container.Value, @"<div\s+class=\"event-name\"[^>]*?>(.*?)</div>", RegexOptions.Singleline);
                var dateMatch = Regex.Match(container.Value, @"<span\s+class=\"time\"\s+data-time=\"([\d]+)\"", RegexOptions.Singleline);

                if (team1Match.Success && team2Match.Success && resultMatch.Success && tournamentMatch.Success && dateMatch.Success)
                {
                    var team1Name = team1Match.Groups[1].Value.Trim();
                    var team2Name = team2Match.Groups[1].Value.Trim();
                    var result = resultMatch.Groups[1].Value.Trim();
                    var tournamentName = tournamentMatch.Groups[1].Value.Trim();
                    var unixTimestamp = long.Parse(dateMatch.Groups[1].Value);
                    var matchDate = DateTimeOffset.FromUnixTimeMilliseconds(unixTimestamp).UtcDateTime;

                    // Determine win/loss (simplified)
                    string matchResult = "DRAW";
                    if (result.Contains("-"))
                    {
                        var scores = result.Split('-').Select(s => int.Parse(s.Trim())).ToArray();
                        if (scores[0] > scores[1]) matchResult = "WIN"; // Assuming team1 wins
                        else if (scores[0] < scores[1]) matchResult = "LOSS"; // Assuming team1 loses
                    }

                    // Dummy values for PlayerId, TeamId, PlayerRating, IsMVP, TournamentTier
                    // In a real scenario, these would need to be resolved from DB or external sources.
                    matches.Add(new Models.Match
                    {
                        TeamId = null, // Needs to be resolved
                        PlayerId = null, // Needs to be resolved
                        Opponent = team2Name, // For team1
                        Result = matchResult, // For team1
                        PlayerRating = null, 
                        IsMVP = false,
                        Tournament = tournamentName,
                        TournamentTier = 1, // Defaulting to Major for now
                        MatchDate = matchDate,
                        CreatedAt = DateTime.UtcNow
                    });
                }
            }
            return matches;
        }
        */

        private async Task<string> GetHtmlWithRetry(string url, int maxRetries = 3, int delayMs = 1000)
        {
            for (int i = 0; i < maxRetries; i++)
            {
                try
                {
                    var response = await _httpClient.GetAsync(url);
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadAsStringAsync();
                }
                catch (HttpRequestException ex)
                {
                    _logger.LogWarning($"Attempt {i + 1} failed for {url}: {ex.Message}");
                    if (i < maxRetries - 1)
                    {
                        await Task.Delay(delayMs);
                    }
                }
            }
            _logger.LogError($"Failed to retrieve HTML from {url} after {maxRetries} attempts.");
            return string.Empty;
        }
    }
}

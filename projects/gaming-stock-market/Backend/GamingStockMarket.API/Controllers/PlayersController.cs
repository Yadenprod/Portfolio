using Microsoft.AspNetCore.Mvc;
using GamingStockMarket.API.DTOs;
using GamingStockMarket.API.Models;
using GamingStockMarket.API.Repositories;
using Microsoft.Extensions.Logging;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using System;
using GamingStockMarket.API.Services.Interfaces; // Added for IPriceCalculator

namespace GamingStockMarket.API.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class PlayersController : ControllerBase
    {
        private readonly IPlayerRepository _playerRepository;
        private readonly ITeamRepository _teamRepository;
        private readonly IPriceCalculator _priceCalculator;
        private readonly ILogger<PlayersController> _logger;

        public PlayersController(IPlayerRepository playerRepository, ITeamRepository teamRepository, IPriceCalculator priceCalculator, ILogger<PlayersController> logger)
        {
            _playerRepository = playerRepository;
            _teamRepository = teamRepository;
            _priceCalculator = priceCalculator;
            _logger = logger;
        }

        [HttpGet]
        [ResponseCache(Duration = 60, Location = ResponseCacheLocation.Any, NoStore = false)] // Cache for 60 seconds
        public async Task<ActionResult<IEnumerable<PlayerResponse>>> GetAllPlayers([FromQuery] string? game = null, [FromQuery] string? searchTerm = null, [FromQuery] int pageNumber = 1, [FromQuery] int pageSize = 10)
        {
            try
            {
                IEnumerable<Models.Player> players;
                if (!string.IsNullOrEmpty(game))
                {
                    players = await _playerRepository.GetActivePlayersByGameAsync(game);
                }
                else
                {
                    players = await _playerRepository.GetAllPlayersWithDetailsAsync();
                    if (!string.IsNullOrEmpty(searchTerm))
                    {
                        players = players.Where(p => p.Name.Contains(searchTerm, StringComparison.OrdinalIgnoreCase) ||
                                                     (p.Team != null && p.Team.Contains(searchTerm, StringComparison.OrdinalIgnoreCase)));
                    }
                    players = players.Skip((pageNumber - 1) * pageSize).Take(pageSize);
                }

                var playerResponses = players.Select(p => new PlayerResponse
                {
                    Id = p.Id,
                    Name = p.Name,
                    Game = p.Game,
                    Team = p.Team,
                    CurrentPrice = p.CurrentPrice,
                    Rating = p.Rating,
                    PopularityScore = p.PopularityScore
                });

                return Ok(playerResponses);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error getting all players.");
                return StatusCode(500, new { message = "Internal server error." });
            }
        }

        [HttpGet("{id}")]
        [ResponseCache(Duration = 60, Location = ResponseCacheLocation.Any, NoStore = false)] // Cache for 60 seconds
        public async Task<ActionResult<PlayerResponse>> GetPlayerById(int id)
        {
            try
            {
                var player = await _playerRepository.GetByIdAsync(id);
                if (player == null) return NotFound(new { message = "Player not found." });

                return Ok(new PlayerResponse
                {
                    Id = player.Id,
                    Name = player.Name,
                    Game = player.Game,
                    Team = player.Team,
                    CurrentPrice = player.CurrentPrice,
                    Rating = player.Rating,
                    PopularityScore = player.PopularityScore
                });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error getting player with ID {PlayerId}.", id);
                return StatusCode(500, new { message = "Internal server error." });
            }
        }

        [HttpGet("teams")]
        public async Task<ActionResult<IEnumerable<TeamResponse>>> GetAllTeams([FromQuery] string? game = null, [FromQuery] string? searchTerm = null, [FromQuery] int pageNumber = 1, [FromQuery] int pageSize = 10)
        {
            try
            {
                IEnumerable<Models.Team> teams;
                if (!string.IsNullOrEmpty(game))
                {
                    teams = await _teamRepository.GetActiveTeamsByGameAsync(game);
                }
                else
                {
                    teams = await _teamRepository.GetAllAsync();
                    if (!string.IsNullOrEmpty(searchTerm))
                    {
                        teams = teams.Where(t => t.Name.Contains(searchTerm, StringComparison.OrdinalIgnoreCase));
                    }
                    teams = teams.Skip((pageNumber - 1) * pageSize).Take(pageSize);
                }

                var teamResponses = teams.Select(t => new TeamResponse
                {
                    Id = t.Id,
                    Name = t.Name,
                    Game = t.Game,
                    CurrentPrice = t.CurrentPrice,
                    Ranking = t.Ranking
                });

                return Ok(teamResponses);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error getting all teams.");
                return StatusCode(500, new { message = "Internal server error." });
            }
        }

        [HttpGet("teams/{id}")]
        public async Task<ActionResult<TeamResponse>> GetTeamById(int id)
        {
            try
            {
                var team = await _teamRepository.GetByIdAsync(id);
                if (team == null) return NotFound(new { message = "Team not found." });

                return Ok(new TeamResponse
                {
                    Id = team.Id,
                    Name = team.Name,
                    Game = team.Game,
                    CurrentPrice = team.CurrentPrice,
                    Ranking = team.Ranking
                });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error getting team with ID {TeamId}.", id);
                return StatusCode(500, new { message = "Internal server error." });
            }
        }
    }
}

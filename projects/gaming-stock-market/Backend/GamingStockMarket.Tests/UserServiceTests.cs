using Xunit;
using Moq;
using FluentAssertions;
using GamingStockMarket.API.Services;
using GamingStockMarket.API.Services.Interfaces;
using GamingStockMarket.API.Repositories;
using GamingStockMarket.API.Models;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;
using System.Threading.Tasks;
using System;
using System.Collections.Generic;

namespace GamingStockMarket.Tests
{
    public class UserServiceTests
    {
        private readonly Mock<IUserRepository> _userRepositoryMock;
        private readonly Mock<IJwtService> _jwtServiceMock;
        private readonly Mock<IEmailService> _emailServiceMock;
        private readonly Mock<ILogger<UserService>> _loggerMock;
        private readonly UserService _userService;

        public UserServiceTests()
        {
            _userRepositoryMock = new Mock<IUserRepository>();
            _jwtServiceMock = new Mock<IJwtService>();
            _emailServiceMock = new Mock<IEmailService>();
            _loggerMock = new Mock<ILogger<UserService>>();

            _userService = new UserService(
                _userRepositoryMock.Object,
                _jwtServiceMock.Object,
                _emailServiceMock.Object,
                _loggerMock.Object
            );
        }

        [Fact]
        public async Task RegisterAsync_ShouldReturnUser_WhenRegistrationIsSuccessful()
        {
            // Arrange
            var username = "testuser";
            var email = "test@example.com";
            var password = "Password123!";
            var newUser = new User { Id = 1, Username = username, Email = email };

            _userRepositoryMock.Setup(r => r.GetByUsernameAsync(username)).ReturnsAsync((User?)null);
            _userRepositoryMock.Setup(r => r.GetByEmailAsync(email)).ReturnsAsync((User?)null);
            _userRepositoryMock.Setup(r => r.AddAsync(It.IsAny<User>())).ReturnsAsync(newUser);
            _emailServiceMock.Setup(e => e.SendEmailAsync(It.IsAny<string>(), It.IsAny<string>(), It.IsAny<string>())).Returns(Task.CompletedTask);

            // Act
            var result = await _userService.RegisterAsync(username, email, password);

            // Assert
            result.Should().BeEquivalentTo(newUser, options => options.Excluding(u => u.PasswordHash));
            _userRepositoryMock.Verify(r => r.AddAsync(It.IsAny<User>()), Times.Once);
            _emailServiceMock.Verify(e => e.SendEmailAsync(It.IsAny<string>(), It.IsAny<string>(), It.IsAny<string>()), Times.Once);
        }

        [Fact]
        public async Task RegisterAsync_ShouldThrowException_WhenUsernameExists()
        {
            // Arrange
            var username = "existinguser";
            var email = "test@example.com";
            var password = "Password123!";

            _userRepositoryMock.Setup(r => r.GetByUsernameAsync(username)).ReturnsAsync(new User { Username = username });

            // Act
            Func<Task> act = async () => await _userService.RegisterAsync(username, email, password);

            // Assert
            await act.Should().ThrowAsync<Exception>().WithMessage("Username already exists.");
            _userRepositoryMock.Verify(r => r.AddAsync(It.IsAny<User>()), Times.Never);
        }

        [Fact]
        public async Task AuthenticateAsync_ShouldReturnJwtToken_WhenCredentialsAreValid()
        {
            // Arrange
            var username = "testuser";
            var password = "Password123!";
            var user = new User { Id = 1, Username = username, PasswordHash = BCrypt.Net.BCrypt.HashPassword(password) };
            var jwtToken = "some.jwt.token";
            var refreshToken = "some_refresh_token";

            _userRepositoryMock.Setup(r => r.GetByUsernameAsync(username)).ReturnsAsync(user);
            _jwtServiceMock.Setup(s => s.GenerateJwtToken(user)).Returns(jwtToken);
            _jwtServiceMock.Setup(s => s.GenerateRefreshToken()).Returns(refreshToken);
            _userRepositoryMock.Setup(r => r.UpdateAsync(It.IsAny<User>())).Returns(Task.CompletedTask);

            // Act
            var result = await _userService.AuthenticateAsync(username, password);

            // Assert
            result.Should().NotBeNull();
            result.JwtToken.Should().Be(jwtToken);
            result.RefreshToken.Should().Be(refreshToken);
            _userRepositoryMock.Verify(r => r.UpdateAsync(It.IsAny<User>()), Times.Once);
        }

        [Fact]
        public async Task AuthenticateAsync_ShouldReturnNull_WhenInvalidCredentials()
        {
            // Arrange
            var username = "testuser";
            var password = "wrongpassword";
            var user = new User { Id = 1, Username = username, PasswordHash = BCrypt.Net.BCrypt.HashPassword("Password123!") };

            _userRepositoryMock.Setup(r => r.GetByUsernameAsync(username)).ReturnsAsync(user);

            // Act
            var result = await _userService.AuthenticateAsync(username, password);

            // Assert
            result.Should().BeNull();
            _userRepositoryMock.Verify(r => r.UpdateAsync(It.IsAny<User>()), Times.Never);
        }
    }
}

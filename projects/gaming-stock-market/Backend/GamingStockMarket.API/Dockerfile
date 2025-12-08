FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /

# Copy API csproj
COPY Backend/GamingStockMarket.API Backend/GamingStockMarket.API

# Restore API dependencies
WORKDIR /Backend/GamingStockMarket.API
RUN dotnet restore GamingStockMarket.API.csproj

# Publish API
RUN dotnet publish GamingStockMarket.API.csproj -c Release -o /app/publish

FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS final
WORKDIR /app
COPY --from=build /app/publish .
ENTRYPOINT ["dotnet", "GamingStockMarket.API.dll"]

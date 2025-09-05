# RocketReach SDK Documentation

This directory contains comprehensive documentation for the RocketReach SDK project.

## 📚 Documentation Structure

### API Documentation
- **[Build SDK for API.md](Build%20SDK%20for%20API.md)** - People Search API reference
- **[RocketReach People Data API – Person Lookup & Person Enrich Endpoints.md](RocketReach%20People%20Data%20API%20%E2%80%93%20Person%20Lookup%20&%20Person%20Enrich%20Endpoints.md)** - Person Lookup and Enrich API reference

### Project Documentation
- **[PROJECT_PLAN.md](PROJECT_PLAN.md)** - Complete project development plan
- **[API_REFERENCE.md](API_REFERENCE.md)** - Comprehensive API reference
- **[DEVELOPMENT_GUIDE.md](DEVELOPMENT_GUIDE.md)** - Development setup and guidelines
- **[TESTING_GUIDE.md](TESTING_GUIDE.md)** - Testing strategies and procedures
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Contribution guidelines
- **[CHANGELOG.md](CHANGELOG.md)** - Version history and changes

### Language-Specific Documentation
- **[PHP/](PHP/)** - PHP SDK specific documentation
- **[Python/](Python/)** - Python SDK specific documentation

## 🚀 Quick Start

1. **Choose your language**: [PHP SDK](../php/README.md) or [Python SDK](../python/README.md)
2. **Get your API key**: [RocketReach Dashboard](https://rocketreach.co/api)
3. **Install the SDK**: Follow the installation instructions for your chosen language
4. **Read the examples**: Check out the examples in each SDK's `examples/` directory

## 📖 API Reference

The RocketReach API provides three main endpoints:

### People Search
Search for professional profiles by various criteria (name, title, company, location, etc.).

**Endpoint**: `POST /api/v2/person/search`
**Documentation**: [Build SDK for API.md](Build%20SDK%20for%20API.md)

### Person Lookup
Retrieve detailed contact information for a specific person.

**Endpoint**: `GET /api/v2/person/lookup`
**Documentation**: [RocketReach People Data API – Person Lookup & Person Enrich Endpoints.md](RocketReach%20People%20Data%20API%20%E2%80%93%20Person%20Lookup%20&%20Person%20Enrich%20Endpoints.md)

### Person Enrich
Get both person and company information in a single call.

**Endpoint**: `GET /api/v2/profile-company/lookup`
**Documentation**: [RocketReach People Data API – Person Lookup & Person Enrich Endpoints.md](RocketReach%20People%20Data%20API%20%E2%80%93%20Person%20Lookup%20&%20Person%20Enrich%20Endpoints.md)

## 🔧 Development

- **Project Plan**: [PROJECT_PLAN.md](PROJECT_PLAN.md)
- **Development Guide**: [DEVELOPMENT_GUIDE.md](DEVELOPMENT_GUIDE.md)
- **Testing Guide**: [TESTING_GUIDE.md](TESTING_GUIDE.md)
- **Contributing**: [CONTRIBUTING.md](CONTRIBUTING.md)

## 📄 License

- **Code**: GNU Affero General Public License v3.0 (see [LICENSE](../LICENSE))
- **Documentation**: Creative Commons Attribution-ShareAlike 4.0 International (see [LICENSE-DOCS](../LICENSE-DOCS))

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/actuallyrizzn/rocketreach-sdk/issues)
- **RocketReach Support**: [RocketReach Support](https://rocketreach.co/support)
- **Documentation Issues**: Please open an issue with the `documentation` label

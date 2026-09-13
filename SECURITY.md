# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Security Architecture Principles

1. **Local-First Privacy**: By default, no personal audio, student essays, transcripts, or mistake logs are ever transmitted over the network.
2. **Zero Telemetry**: No tracking beacons, analytics pings, or background telemetry exist in the application.
3. **SSRF and Network Boundaries**: The online research module strictly restricts outbound requests, implements tight timeouts, and extracts only compact text snippets.
4. **SQL Parameterization**: All interactions with SQLite use strictly parameterized queries to prevent SQL injection vulnerabilities.
5. **No Executable Code in Prompts**: The AI Tutor never executes system terminal commands on behalf of user prompt inputs.

## Reporting a Vulnerability

If you discover a security vulnerability within IELTS by GAMA, please submit an issue with the label `security` or contact the development team securely. Responsible disclosures will receive prompt response within 48 hours.

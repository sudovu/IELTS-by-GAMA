# Contributing to IELTS by GAMA

Thank you for your interest in contributing to **IELTS by GAMA**!

## Development Guidelines

1. **Maintain Offline Independence**: Every core curriculum feature must function completely offline with zero external network connectivity.
2. **Copyright Compliance**: Never submit copyrighted Cambridge/IELTS practice questions, passages, or proprietary materials. All pedagogical practice content must be 100% original.
3. **Memory & Storage Minimization**: Follow the memory tiering policy:
   - HOT DATA in RAM
   - Temporary cache with TTL/LRU
   - Compact permanent knowledge in SQLite.
4. **Code Quality**: Ensure all tests pass before opening a PR:
   ```bash
   python -m unittest discover tests
   ```

## Pull Request Process

1. Fork the repository and create your branch from `main`.
2. Implement your feature or fix.
3. Add or update unit tests in `tests/`.
4. Ensure all tests pass and documentation is updated.
5. Submit a pull request with a clear description of the pedagogical or technical improvement.

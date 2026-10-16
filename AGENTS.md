# Working preferences

- Make repository changes on a feature branch and open or update a pull request. Do not push directly to the default branch, merge a PR, or rewrite shared history unless explicitly requested.
- Use `Codex` as the Git author and committer name for commits you create. Keep the configured email unless instructed otherwise; prefer repository-local Git configuration.
- Keep changes minimal and within the requested scope. Do not add, remove, or rewrite existing comments, including inline comments, unless explicitly requested.
- Run checks appropriate to the change and report what passed and what remains unverified. Keep PR titles and descriptions accurate to the final scope.

# Protocol emulator repository

For work on `abeinn/protocol-emu`:

- Read the original article before making project decisions: https://blog.janestreet.com/protocol-emulator-asic-competition/ . Follow its link to the original CMOS5L Verilog template and verify relevant requirements against the current sources.
- In the initial setup PR, Verilog changes must be limited to the top-module declaration and corresponding instantiation names. Do not change the example logic.
- Use branches and PRs for subsequent work. Keep the current PR's scope constraints separate from later explicitly requested implementation work.

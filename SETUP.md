# Setup

1. The repository must be **public** and named exactly `ljj13/ljj13` so GitHub can render the Profile README.

2. Open the repository's **Actions** tab and manually run:
   - `Generate contribution snake`
   - `Generate 3D contribution calendar`

3. After the snake workflow finishes, verify that an `output` branch exists.

4. After the 3D workflow finishes, verify that `profile-3d-contrib/` exists on the default branch.

5. Visit `https://github.com/ljj13` and confirm the profile README is rendered.

## Notes

- GitHub Actions needs repository workflow permission to write contents.
- If Actions cannot push, open: Settings → Actions → General → Workflow permissions, then select **Read and write permissions**.
- The public GitHub Readme Stats instance is best-effort; if it later rate-limits, self-hosting is the reliable fallback.
- The page intentionally avoids trophy walls, Spotify widgets and profile-view counters to keep the profile clean.

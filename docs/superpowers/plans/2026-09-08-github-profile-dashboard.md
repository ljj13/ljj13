# GitHub Profile Dashboard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the full experimental FogPurification GitHub Profile dashboard with all requested non-WakaTime/non-Spotify/non-RSS widgets, favoring repository-generated assets and excluding broken images.

**Architecture:** Keep README presentation separate from asset generation. Repository-local Actions generate stable Stats/Top Languages and existing Snake/3D assets; verified external SVG services provide Streak, Activity Graph, Trophy, typing, icons, badges and profile views. Summary Cards and Metrics use their public or Action implementations only when verification succeeds without a user-supplied PAT.

**Tech Stack:** GitHub Profile README, GitHub Actions, SVG, Shields.io, Platane/snk, github-profile-3d-contrib, github-readme-stats-fast-action, github-profile-summary-cards, lowlighter/metrics.

**Spec:** `docs/superpowers/specs/2026-09-08-github-profile-dashboard-design.md`

## Global Constraints

- Never show the user's real name.
- Display identity is exactly `FogPurification`.
- Current GitHub username remains `ljj13` for URLs and APIs until the user changes the account username.
- Do not leave a known-broken image in README.
- Do not ask the user for a PAT, WakaTime, Spotify, or RSS credentials.
- Keep current Snake and 3D automations working.

---

### Task 1: Generate stable GitHub stats assets

**Files:**
- Create: `.github/workflows/profile-stats.yml`
- Produce at runtime: `profile-assets/github-stats.svg`
- Produce at runtime: `profile-assets/top-languages.svg`

**Interfaces:**
- Consumes: repository-scoped `${{ secrets.GITHUB_TOKEN }}`.
- Produces: two SVG files referenced directly by README.

- [ ] **Step 1: Create workflow** using `Pranesh-2005/github-readme-stats-fast-action@v1.3`, `permissions: contents: write`, two cards, and a commit/push step.
- [ ] **Step 2: Add `workflow_dispatch`, daily schedule, and self-test `push.paths` trigger.**
- [ ] **Step 3: Trigger via the workflow-file push and inspect the run.**
- [ ] **Step 4: Verify both generated SVG files exist on `main`.**

### Task 2: Add Profile Summary Cards

**Files:**
- Create: `.github/workflows/profile-summary-cards.yml` if Action mode succeeds.
- Runtime output: `profile-summary-card-output/` if Action mode succeeds.

**Interfaces:**
- Consumes: repository token first; hosted API is fallback.
- Produces: Profile Details, Repos-per-language, Stats/Productive Time style summary cards or equivalent hosted URLs.

- [ ] **Step 1: Try the upstream Action using `${{ secrets.GITHUB_TOKEN }}`.**
- [ ] **Step 2: Inspect the run and generated files.**
- [ ] **Step 3: If account-level queries reject the repository token, remove the failing workflow and use verified hosted API URLs instead.**
- [ ] **Step 4: Ensure README will not reference a non-existent local summary-card path.**

### Task 3: Verify external widget endpoints

**Files:**
- No repository file yet.

**Interfaces:**
- Consumes: public widget endpoints for user `ljj13`.
- Produces: a final allow-list of external URLs that return image content.

- [ ] **Step 1: Verify Streak endpoint (`streak-stats.demolab.com`).**
- [ ] **Step 2: Verify Activity Graph endpoint (`github-readme-activity-graph.vercel.app`).**
- [ ] **Step 3: Verify Trophy endpoint (`github-profile-trophy.vercel.app`).**
- [ ] **Step 4: Verify Typing SVG, Skill Icons, Shields, and Profile Views endpoints.**
- [ ] **Step 5: Verify public lowlighter Metrics endpoint; if invalid, exclude the image rather than shipping a break.**

### Task 4: Rebuild README layout

**Files:**
- Modify: `README.md`

**Interfaces:**
- Consumes: local generated assets from Tasks 1/2 and verified external endpoints from Task 3.
- Produces: final Profile README.

- [ ] **Step 1: Replace hero with avatar + `FogPurification` + Chinese slogan + typing SVG + Website/GitHub buttons + profile views.**
- [ ] **Step 2: Keep ABOUT concise and free of real-name references.**
- [ ] **Step 3: Expand TECH STACK with Skill Icons plus restrained Shields badges.**
- [ ] **Step 4: Keep PROJECT LAB in a two-column table.**
- [ ] **Step 5: Add GITHUB OVERVIEW with local Stats/Top Languages, Streak and Summary Cards.**
- [ ] **Step 6: Add ACTIVITY with Activity Graph and one-row Trophy.**
- [ ] **Step 7: Add METRICS only if a verified image source exists.**
- [ ] **Step 8: Keep Snake and 3D sections at the bottom.**

### Task 5: End-to-end verification

**Files:**
- Read: `README.md`
- Read: `.github/workflows/*.yml`
- Read: generated SVG assets.

**Interfaces:**
- Consumes: final repository state.
- Produces: evidence that the profile is ready.

- [ ] **Step 1: Search README for the user's real name and confirm zero matches.**
- [ ] **Step 2: Confirm no `github-readme-stats.vercel.app` URL remains.**
- [ ] **Step 3: Confirm local stats, Snake, and 3D SVGs exist.**
- [ ] **Step 4: Confirm all new workflow runs finish successfully or remove any failing optional workflow.**
- [ ] **Step 5: Re-read README and verify section order, links, and image sources.**

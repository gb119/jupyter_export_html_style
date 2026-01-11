# GitHub Pages Setup Instructions

This document provides instructions for setting up GitHub Pages to receive and publish the built HTML documentation from the `docs.yml` workflow.

## Prerequisites

- Repository admin access
- The `docs.yml` workflow has been configured to deploy to GitHub Pages (completed)

## Steps to Enable GitHub Pages

1. **Navigate to Repository Settings**
   - Go to the repository on GitHub: https://github.com/gb119/jupyter_export_html_style
   - Click on **Settings** tab
   - In the left sidebar, click on **Pages** (under "Code and automation")

2. **Configure GitHub Pages Source**
   - Under "Build and deployment" section
   - Set **Source** to: **GitHub Actions**
   - This allows the workflow to deploy directly to GitHub Pages

3. **Verify the Configuration**
   - The workflow will automatically deploy on the next push to the `main` branch
   - Or you can manually trigger it using the "Run workflow" button in the Actions tab

4. **Access Your Documentation**
   - After the first successful deployment, your documentation will be available at:
     - `https://gb119.github.io/jupyter_export_html_style/`
   - The URL will also be visible in the workflow run under the "Deploy to GitHub Pages" step

## What the Workflow Does

The `docs.yml` workflow now:

1. **Builds the Documentation**: Uses Sphinx to build HTML documentation from the `docs/` directory
2. **Creates .nojekyll File**: Ensures GitHub Pages serves all files correctly (including files starting with underscore)
3. **Uploads Artifact**: Packages the built HTML as a GitHub Pages artifact
4. **Deploys to GitHub Pages**: Publishes the artifact to the GitHub Pages environment

## Workflow Permissions

The workflow has been configured with the necessary permissions:
- `contents: read` - To read the repository content
- `pages: write` - To deploy to GitHub Pages
- `id-token: write` - For OIDC authentication with GitHub Pages

## Concurrency Control

The workflow includes concurrency control to:
- Prevent multiple simultaneous deployments
- Allow in-progress deployments to complete (no cancellation)
- Queue new deployments when one is already running

## Troubleshooting

If you encounter issues:

1. **Check Workflow Status**: Go to Actions tab and verify the workflow completed successfully
2. **Verify Pages Settings**: Ensure the source is set to "GitHub Actions" in repository settings
3. **Check Permissions**: Verify the repository has GitHub Pages enabled and the workflow has necessary permissions
4. **Review Logs**: Check the workflow logs for any error messages

## Additional Resources

- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [Configuring a publishing source for GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)
- [Using GitHub Actions with GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)

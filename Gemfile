source "https://rubygems.org"

# The `github-pages` gem pins Jekyll and every plugin to exactly the versions
# GitHub Pages runs, so a local preview matches the deployed build. It is only
# needed for previewing — GitHub builds the site server-side from _config.yml.
#
# Pin the major version. Left unpinned, Bundler can resolve backwards to a very
# old release (Jekyll 3.6 / kramdown 1.14) that fails on modern Ruby because it
# requires `rexml`, which is no longer a default gem.
#
# github-pages brings jekyll-remote-theme, jekyll-include-cache, jekyll-feed,
# jekyll-sitemap and jekyll-seo-tag with it — declaring those separately only
# risks version conflicts.
gem "github-pages", "~> 232", group: :jekyll_plugins

# No longer default gems in Ruby 3.x, still expected by parts of the toolchain.
gem "rexml"
gem "csv"
gem "base64"
gem "bigdecimal"
gem "logger"

# Windows / JRuby timezone data
platforms :mingw, :x64_mingw, :mswin, :jruby do
  gem "tzinfo", ">= 1", "< 3"
  gem "tzinfo-data"
end

gem "wdm", "~> 0.1", platforms: [:mingw, :x64_mingw, :mswin]

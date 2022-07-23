#!/bin/sh

# Install the version of Bundler.
if [ -f Gemfile.lock ] && grep "BUNDLED WITH" Gemfile.lock > /dev/null; then
    cat Gemfile.lock | tail -n 2 | grep -C2 "BUNDLED WITH" | tail -n 1 | xargs gem install bundler -v
fi

# If there's a Gemfile, then run `bundle install`
# It's assumed that the Gemfile will install Jekyll too
if [ -f Gemfile ]; then
    bundle install
fi

if which tldr > /dev/null; then
    echo "installing tldr..."
    mkdir -p /home/vscode/.local/share/
    tldr -u
    echo "tldr installed"
else
    echo "tldr is not installed. Please install it to use the tldr command."
fi
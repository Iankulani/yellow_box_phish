#!/bin/sh

echo "🐠 Starting YellowBoxPhish v2.0.0"
echo "📦 Container: Alpine Linux $(cat /etc/alpine-release)"
echo "🐍 Python: $(python3 --version)"

# Check if running as root for advanced features
if [ "$(id -u)" = "0" ]; then
    echo "⚠️ Running as root - full features available"
else
    echo "⚠️ Running as non-root - some features may be limited"
fi

# Execute the main application
exec "$@"
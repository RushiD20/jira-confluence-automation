# Module 13 Completion Report 
 
## MCP Configuration 
{ 
  "servers": { 
    "my-server": { 
      "command": "powershell", 
      "args": [ 
        "-NoProfile", 
        "-ExecutionPolicy", 
        "Bypass", 
        "-File", 
        "${workspaceFolder}/tools/my-server.ps1" 
      ], 
      "env": { 
        "API_KEY": "[REDACTED_API_KEY]" 
      } 
    },
    "api-server": { 
      "command": "powershell", 
      "args": [ 
        "-NoProfile", 
        "-ExecutionPolicy", 
        "Bypass", 
        "-File", 
        "${workspaceFolder}/tools/api-server.ps1" 
      ], 
      "env": { 
        "API_KEY": "[REDACTED_API_KEY]" 
      } 
    } 
  } 
} 
 
## Configured Servers 
- my-server 
- api-server 
 
## MCP Tool Test 
- Tool used: get_time 
- Output: 
2026-09-16 10:51:32 +05:30 
- API keys: Present and redacted for security 
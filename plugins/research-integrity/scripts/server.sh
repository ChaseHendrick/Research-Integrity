#!/bin/bash
# Local MCP server. This file is the whole command.
# It starts no other program, opens no file, and opens no network connection.
shopt -s nocasematch
while IFS= read -r line || [[ -n $line ]]; do
  if [[ -z $line ]]; then
    continue
  fi
  if [[ $line =~ notifications/ ]]; then
    continue
  fi
  id=""
  if [[ $line =~ \"id\":[[:space:]]*([0-9]+) ]]; then
    id=${BASH_REMATCH[1]}
  fi
  if [[ -z $id ]]; then
    continue
  fi
  if [[ $line =~ '"method":"tools/call"' || $line =~ '"method": "tools/call"' ]]; then
    hits=""
    if [[ $line =~ "this is the first" ]]; then hits='{\"phrase\":\"this is the first\"}'; fi
    if [[ $line =~ "no prior work exists" ]]; then
      if [[ -n $hits ]]; then hits="$hits"',{\"phrase\":\"no prior work exists\"}'; else hits='{\"phrase\":\"no prior work exists\"}'; fi
    fi
    if [[ $line =~ "independently reviewed" ]]; then
      if [[ -n $hits ]]; then hits="$hits"',{\"phrase\":\"independently reviewed\"}'; else hits='{\"phrase\":\"independently reviewed\"}'; fi
    fi
    if [[ $line =~ "externally reviewed" ]]; then
      if [[ -n $hits ]]; then hits="$hits"',{\"phrase\":\"externally reviewed\"}'; else hits='{\"phrase\":\"externally reviewed\"}'; fi
    fi
    if [[ $line =~ "we are not aware" ]]; then
      if [[ -n $hits ]]; then hits="$hits"',{\"phrase\":\"we are not aware\"}'; else hits='{\"phrase\":\"we are not aware\"}'; fi
    fi
    printf '%s\n' "{\"jsonrpc\":\"2.0\",\"id\":$id,\"result\":{\"content\":[{\"type\":\"text\",\"text\":\"{\\\"hits\\\":[$hits],\\\"not_claimed\\\":\\\"A hit is not proof the sentence is false.\\\"}\"}],\"isError\":false}}"
    continue
  fi
  if [[ $line =~ '"method":"tools/list"' || $line =~ '"method": "tools/list"' ]]; then
    printf '%s\n' "{\"jsonrpc\":\"2.0\",\"id\":$id,\"result\":{\"tools\":[{\"name\":\"scan_text\",\"description\":\"Report overclaim phrases in a passage. A hit is not proof the sentence is false. No network.\",\"inputSchema\":{\"type\":\"object\",\"properties\":{\"text\":{\"type\":\"string\"}},\"required\":[\"text\"]}}]}}"
    continue
  fi
  if [[ $line =~ '"method":"initialize"' || $line =~ '"method": "initialize"' ]]; then
    printf '%s\n' "{\"jsonrpc\":\"2.0\",\"id\":$id,\"result\":{\"protocolVersion\":\"2024-11-05\",\"capabilities\":{\"tools\":{}},\"serverInfo\":{\"name\":\"research-integrity\",\"version\":\"1.4.3\"}}}"
    continue
  fi
  if [[ $line =~ '"method":"ping"' || $line =~ '"method": "ping"' ]]; then
    printf '%s\n' "{\"jsonrpc\":\"2.0\",\"id\":$id,\"result\":{}}"
    continue
  fi
  printf '%s\n' "{\"jsonrpc\":\"2.0\",\"id\":$id,\"error\":{\"code\":-32601,\"message\":\"method not found\"}}"
done

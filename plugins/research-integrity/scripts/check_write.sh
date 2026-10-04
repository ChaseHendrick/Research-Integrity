#!/bin/bash
# Phrase warning for Write and Edit. This file is the whole command.
# It starts no other program and builds no path.
shopt -s nocasematch
block=0
if [[ -f .research-integrity.json ]]; then
  while IFS= read -r line || [[ -n $line ]]; do
    if [[ $line =~ '"block": true' || $line =~ '"block":true' ]]; then
      block=1
    fi
  done < .research-integrity.json
fi
hit_first=0
hit_prior=0
hit_independent=0
hit_external=0
hit_aware=0
while IFS= read -r line || [[ -n $line ]]; do
  if [[ $line =~ "this is the first" ]]; then hit_first=1; fi
  if [[ $line =~ "no prior work exists" ]]; then hit_prior=1; fi
  if [[ $line =~ "independently reviewed" ]]; then hit_independent=1; fi
  if [[ $line =~ "externally reviewed" ]]; then hit_external=1; fi
  if [[ $line =~ "we are not aware" ]]; then hit_aware=1; fi
done
found=""
if [[ $hit_first -eq 1 ]]; then found="this is the first"; fi
if [[ $hit_prior -eq 1 ]]; then
  if [[ -n $found ]]; then found="$found, no prior work exists"; else found="no prior work exists"; fi
fi
if [[ $hit_independent -eq 1 ]]; then
  if [[ -n $found ]]; then found="$found, independently reviewed"; else found="independently reviewed"; fi
fi
if [[ $hit_external -eq 1 ]]; then
  if [[ -n $found ]]; then found="$found, externally reviewed"; else found="externally reviewed"; fi
fi
if [[ $hit_aware -eq 1 ]]; then
  if [[ -n $found ]]; then found="$found, we are not aware"; else found="we are not aware"; fi
fi
if [[ -z $found ]]; then
  exit 0
fi
if [[ $block -eq 1 ]]; then
  echo "Blocked write. Overclaim phrase: $found. A hit is not proof the sentence is false." >&2
  exit 2
fi
echo "Overclaim phrase, not blocked: $found. The write proceeded." >&2
exit 0

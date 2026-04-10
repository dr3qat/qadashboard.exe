#!/usr/bin/env bash
# Claude Code status line — replica do layout do screenshot
# Linha 1: cwd = +adds -dels = $custo = tempo
# Linha 2: Modelo • Cx [barra] X% • 5h [barra] X% ©countdown • 7d [barra] X% ©countdown

input=$(cat)

# --- Dados do JSON ---
cwd=$(echo "$input"        | jq -r '.workspace.current_dir // .cwd // ""')
model=$(echo "$input"      | jq -r '.model.display_name // .model.id // "Claude"')
context_used=$(echo "$input" | jq -r '.context_window.used_percentage // empty')
five_pct=$(echo "$input"   | jq -r '.rate_limits.five_hour.used_percentage  // empty')
five_reset=$(echo "$input" | jq -r '.rate_limits.five_hour.resets_at        // empty')
week_pct=$(echo "$input"   | jq -r '.rate_limits.seven_day.used_percentage  // empty')
week_reset=$(echo "$input" | jq -r '.rate_limits.seven_day.resets_at        // empty')
transcript=$(echo "$input" | jq -r '.transcript_path // empty')

# --- Mini barra de progresso (8 blocos unicode) ---
bar() {
  local pct=${1:-0}
  local filled=$(( pct * 8 / 100 ))
  local b="" i=0
  while [ $i -lt $filled ]; do b="${b}█"; i=$(( i + 1 )); done
  while [ $i -lt 8 ];       do b="${b}░"; i=$(( i + 1 )); done
  printf '%s' "$b"
}

# Converte epoch Unix em countdown legivel
hm() {
  local now
  now=$(date +%s)
  local secs=$(( $1 - now ))
  [ "$secs" -le 0 ] && echo "now" && return
  local d=$(( secs / 86400 ))
  local h=$(( (secs % 86400) / 3600 ))
  local m=$(( (secs % 3600) / 60 ))
  if [ "$d" -gt 0 ]; then
    printf '%dd%dh' "$d" "$h"
  elif [ "$h" -gt 0 ]; then
    printf '%dh%02dm' "$h" "$m"
  else
    printf '%dm' "$m"
  fi
}

# --- Git diff stats (+adds -dels) ---
git_stats=""
if [ -n "$cwd" ] && git -C "$cwd" rev-parse --git-dir >/dev/null 2>&1; then
  added=0; removed=0; sa=0; sr=0
  while IFS=$'\t' read -r a r _; do
    added=$(( added + a )); removed=$(( removed + r ))
  done < <(git -C "$cwd" diff --no-lock-index --numstat 2>/dev/null)
  while IFS=$'\t' read -r a r _; do
    sa=$(( sa + a )); sr=$(( sr + r ))
  done < <(git -C "$cwd" diff --no-lock-index --cached --numstat 2>/dev/null)
  total_a=$(( added + sa ))
  total_r=$(( removed + sr ))
  [ "$(( total_a + total_r ))" -gt 0 ] && git_stats=" = +${total_a} -${total_r}"
fi

# --- Custo via ccusage (ferramenta externa opcional) ---
cost_str=""
if command -v ccusage >/dev/null 2>&1; then
  cost_raw=$(ccusage session 2>/dev/null | grep -oE '\$[0-9]+\.[0-9]+' | head -1)
  [ -n "$cost_raw" ] && cost_str=" = ${cost_raw}"
fi

# --- Tempo de sessao pelo transcript ---
session_str=""
if [ -n "$transcript" ] && [ -f "$transcript" ]; then
  start_epoch=$(date -r "$transcript" +%s 2>/dev/null \
             || stat -c %Y "$transcript" 2>/dev/null)
  if [ -n "$start_epoch" ]; then
    elapsed=$(( $(date +%s) - start_epoch ))
    eh=$(( elapsed / 3600 ))
    em=$(( elapsed / 60 ))
    if [ "$eh" -gt 0 ]; then
      session_str=" = ${eh}h$(( (elapsed % 3600) / 60 ))m"
    else
      session_str=" = ${em}m"
    fi
  fi
fi

# === LINHA 1 ===
line1="${cwd}${git_stats}${cost_str}${session_str}"

# === LINHA 2 ===
line2="${model}"

# Context window
if [ -n "$context_used" ]; then
  cx_int=${context_used%.*}
  line2="${line2} • Cx $(bar "$cx_int") ${cx_int}%"
fi

# Rate limit 5h
if [ -n "$five_pct" ]; then
  f_int=${five_pct%.*}
  f_bar=$(bar "$f_int")
  if [ -n "$five_reset" ]; then
    line2="${line2} • 5h ${f_bar} ${f_int}% ©$(hm "$five_reset")"
  else
    line2="${line2} • 5h ${f_bar} ${f_int}%"
  fi
fi

# Rate limit 7d
if [ -n "$week_pct" ]; then
  w_int=${week_pct%.*}
  w_bar=$(bar "$w_int")
  if [ -n "$week_reset" ]; then
    line2="${line2} • 7d ${w_bar} ${w_int}% ©$(hm "$week_reset")"
  else
    line2="${line2} • 7d ${w_bar} ${w_int}%"
  fi
fi

printf '%s\n%s\n' "$line1" "$line2"

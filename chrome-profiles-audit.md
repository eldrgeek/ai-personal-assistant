# Chrome Profiles Storage Audit

## Summary
**Total Chrome Storage Usage: ~11.4GB**

---

## Standard Chrome Profiles (5.0GB Total)
Located in: `~/Library/Application Support/Google/Chrome/`

| Profile | User/Name | Size |
|---------|-----------|------|
| Default | Mike Lavender | 3.2G |
| Profile 30 | Mike Personal | 739M |
| Profile 5 | embeddedsystemsresearch.org | 343M |
| Profile 1 | Bobbi | 310M |
| Profile 15 | joyofinternet.com | 101M |
| Profile 35 | mike-wolf.com | 67M |
| Profile 32 | ulitas.org | 65M |
| Profile 14 | mike-wolf.com | 53M |
| Profile 31 | joyofinternet.com | 35M |
| Profile 26 | yeshid.com | 18M |
| Profile 33 | mike-wolf.com | 16M |
| Profile 34 | Michael B Wolf | 8.1M |
| Profile 18 | joyofinternet.com | 7.1M |
| Profile 36 | embeddedsystemsresearch.org | 5.7M |

### Profile Groups by Domain/User:
- **mike-wolf.com**: 3 profiles (136M total)
- **joyofinternet.com**: 3 profiles (143.1M total)
- **embeddedsystemsresearch.org**: 2 profiles (348.7M total)
- **Personal/Named**: Mike Lavender (3.2G), Mike Personal (739M), Bobbi (310M), Michael B Wolf (8.1M)
- **Other domains**: yeshid.com (18M), ulitas.org (65M)

---

## Development Chrome Profiles (6.4GB Total)
Located in: `~/Projects/*/chrome-debug-profile/`

| Project | Path | Size |
|---------|------|------|
| Plasmo | ~/Projects/Plasmo/chrome-debug-profile | 3.5G |
| FrontRow | ~/Projects/FrontRow/chrome-debug-profile | 2.7G |
| YeshDesign | ~/Projects/YeshDesign/chrome-debug-profile | 301M |

---

## Storage Breakdown

### By Type:
- **Standard Profiles**: 5.0GB (44%)
- **Development Profiles**: 6.4GB (56%)

### Largest Space Users:
1. Plasmo debug profile: 3.5G
2. Default (Mike Lavender): 3.2G
3. FrontRow debug profile: 2.7G
4. Profile 30 (Mike Personal): 739M
5. Profile 5 (embeddedsystemsresearch.org): 343M

---

## Recommendations for Space Recovery

### Quick Wins (minimal impact):
- Clear cache/history in Default profile (could save ~1-2GB)
- Remove unused development profiles if projects are complete

### Medium Impact:
- Archive or remove duplicate domain profiles (mike-wolf.com has 3 profiles)
- Consolidate joyofinternet.com profiles (3 profiles totaling 143.1M)

### High Impact:
- Remove Plasmo debug profile if not actively developing (3.5G)
- Remove FrontRow debug profile if not actively developing (2.7G)
- Clean up Default profile or migrate to a smaller profile (3.2G)

---

*Generated: August 28, 2024*
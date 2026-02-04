#!/usr/bin/env python3
"""
Cost calculator for meeting summarizer
Helps estimate monthly costs based on usage
"""

def calculate_cost(num_meetings, avg_duration_minutes):
    """
    Calculate estimated costs

    Args:
        num_meetings: Number of meetings per month
        avg_duration_minutes: Average meeting duration in minutes

    Returns:
        dict with cost breakdown
    """
    # Pricing (as of 2024)
    WHISPER_COST_PER_MINUTE = 0.006  # $0.006 per minute
    CLAUDE_INPUT_COST_PER_1K = 0.003  # $3 per MTok = $0.003 per 1K tokens
    CLAUDE_OUTPUT_COST_PER_1K = 0.015  # $15 per MTok = $0.015 per 1K tokens

    # Estimates
    TOKENS_PER_MINUTE = 150  # Approximate tokens in transcript per minute
    OUTPUT_TOKENS = 500  # Approximate output tokens for summary

    # Calculate costs
    total_minutes = num_meetings * avg_duration_minutes

    # Whisper cost
    whisper_cost = total_minutes * WHISPER_COST_PER_MINUTE

    # Claude cost
    input_tokens = total_minutes * TOKENS_PER_MINUTE
    claude_input_cost = (input_tokens / 1000) * CLAUDE_INPUT_COST_PER_1K
    claude_output_cost = (OUTPUT_TOKENS * num_meetings / 1000) * CLAUDE_OUTPUT_COST_PER_1K
    claude_cost = claude_input_cost + claude_output_cost

    # Total cost
    total_cost = whisper_cost + claude_cost

    return {
        'num_meetings': num_meetings,
        'avg_duration_minutes': avg_duration_minutes,
        'total_minutes': total_minutes,
        'whisper_cost': whisper_cost,
        'claude_cost': claude_cost,
        'total_cost': total_cost,
        'cost_per_meeting': total_cost / num_meetings if num_meetings > 0 else 0
    }


def print_cost_breakdown(costs):
    """Print formatted cost breakdown"""
    print("\n" + "=" * 60)
    print("COST ESTIMATE")
    print("=" * 60)
    print(f"\nUsage:")
    print(f"  Meetings per month: {costs['num_meetings']}")
    print(f"  Average duration: {costs['avg_duration_minutes']} minutes")
    print(f"  Total minutes: {costs['total_minutes']}")

    print(f"\nCost Breakdown:")
    print(f"  Whisper (transcription): ${costs['whisper_cost']:.2f}")
    print(f"  Claude (analysis): ${costs['claude_cost']:.2f}")
    print(f"  {'─' * 40}")
    print(f"  Total monthly cost: ${costs['total_cost']:.2f}")
    print(f"  Cost per meeting: ${costs['cost_per_meeting']:.2f}")

    print(f"\nWith 50% cache hit rate:")
    print(f"  Estimated cost: ${costs['total_cost'] * 0.75:.2f}/month")
    print(f"  (Cached transcripts save ~50% on Whisper costs)")

    print("\n" + "=" * 60)


def compare_with_alternatives():
    """Compare with alternative services"""
    print("\n" + "=" * 60)
    print("COMPARISON WITH ALTERNATIVES")
    print("=" * 60)

    alternatives = [
        {
            'name': 'Fireflies.ai',
            'cost': 10,
            'notes': 'Basic plan, limited features'
        },
        {
            'name': 'Otter.ai',
            'cost': 16.99,
            'notes': 'Pro plan, 6000 minutes/year'
        },
        {
            'name': 'Grain',
            'cost': 15,
            'notes': 'Starter plan'
        },
        {
            'name': 'This Solution',
            'cost': 8,
            'notes': 'Pay-as-you-go, 20 meetings/month'
        }
    ]

    print("\nMonthly Cost Comparison:")
    for alt in alternatives:
        marker = "👉" if alt['name'] == 'This Solution' else "  "
        print(f"{marker} {alt['name']:<20} ${alt['cost']:>6.2f}/month  ({alt['notes']})")

    print("\nAdvantages of this solution:")
    print("  ✓ No monthly subscription")
    print("  ✓ Pay only for what you use")
    print("  ✓ Full control over code and data")
    print("  ✓ Customizable analysis")
    print("  ✓ Best-in-class AI (Whisper + Claude)")
    print("  ✓ Local caching saves costs")

    print("=" * 60)


def main():
    print("=" * 60)
    print("Meeting Summarizer - Cost Calculator")
    print("=" * 60)

    # Get user input
    try:
        num_meetings = int(input("\nHow many meetings per month? (default: 20): ") or "20")
        avg_duration = int(input("Average meeting duration in minutes? (default: 60): ") or "60")
    except ValueError:
        print("Invalid input. Using defaults: 20 meetings, 60 minutes each")
        num_meetings = 20
        avg_duration = 60

    # Calculate costs
    costs = calculate_cost(num_meetings, avg_duration)

    # Print breakdown
    print_cost_breakdown(costs)

    # Compare with alternatives
    compare_with_alternatives()

    # Additional scenarios
    print("\n" + "=" * 60)
    print("OTHER SCENARIOS")
    print("=" * 60)

    scenarios = [
        (10, 30, "Light usage (10 short meetings)"),
        (20, 60, "Medium usage (20 hour-long meetings)"),
        (40, 45, "Heavy usage (40 meetings, 45 min each)"),
        (100, 30, "Enterprise usage (100 short meetings)")
    ]

    for meetings, duration, description in scenarios:
        costs = calculate_cost(meetings, duration)
        print(f"\n{description}:")
        print(f"  ${costs['total_cost']:.2f}/month (${costs['cost_per_meeting']:.2f} per meeting)")

    print("\n" + "=" * 60)
    print("\nTips to reduce costs:")
    print("  1. Enable caching (already enabled by default)")
    print("  2. Use batch processing instead of real-time monitoring")
    print("  3. Only process important meetings")
    print("  4. Shorter meetings = lower costs")
    print("=" * 60)


if __name__ == '__main__':
    main()

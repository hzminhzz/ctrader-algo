using cAlgo.API;

namespace Ctrader.Bots;

[Robot(TimeZone = TimeZones.UTC, AccessRights = AccessRights.None)]
public class BreakoutBot : Robot
{
    [Parameter("Breakout Lookback", DefaultValue = 20)]
    public int BreakoutLookback { get; set; }

    [Parameter("Risk Per Trade", DefaultValue = 0.01)]
    public double RiskPerTrade { get; set; }

    [Parameter("Session Filter", DefaultValue = "London")]
    public string SessionFilter { get; set; } = "London";

    [Parameter("Stop Loss", DefaultValue = 20)]
    public int StopLoss { get; set; }

    [Parameter("Take Profit", DefaultValue = 40)]
    public int TakeProfit { get; set; }

    protected override void OnStart()
    {
    }

    protected override void OnBar()
    {
        var shouldTrade = false;

        if (!shouldTrade)
        {
            return;
        }
    }
}

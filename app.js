const demoSectors = [
  {
    name: "Meme",
    description: "DOGE, SHIB, PEPE, FLOKI, BONK, WIF.",
    rank: 91,
    index: 65.94,
    perf5m: 0.1,
    perf1h: 4.1,
    perf24h: -34.06,
    volume24h: 9200000000,
    liqUsd: 1140000000,
    liqPct: 12.4,
    longPct: 63,
    shortPct: 37,
    oiUsd: 2800000000,
    oiChange: 4.8,
    cvd: 42000000,
    tokens: [
      { symbol: "DOGE", price: 0.11025, perf24h: 1.82, volume: 1037512960 },
      { symbol: "SHIB", price: 0.000006599, perf24h: 2.29, volume: 84061067 },
      { symbol: "PEPE", price: 0.000004352, perf24h: 2.1, volume: 469084529 },
      { symbol: "FLOKI", price: 0.00003713, perf24h: 2.12, volume: 13559370 },
      { symbol: "BONK", price: 0.000007594, perf24h: 4.26, volume: 98665556 },
      { symbol: "WIF", price: 0.2284, perf24h: 1.42, volume: 57089757 }
    ]
  },
  {
    name: "AI",
    description: "RNDR, FET, AGIX, OCEAN, AKT.",
    rank: 86,
    index: 80.87,
    perf5m: 0.63,
    perf1h: 3.82,
    perf24h: -19.13,
    volume24h: 3800000000,
    liqUsd: 259000000,
    liqPct: 6.83,
    longPct: 55,
    shortPct: 45,
    oiUsd: 1250000000,
    oiChange: 8.1,
    cvd: 31000000,
    tokens: [
      { symbol: "RNDR", price: 8.14, perf24h: -20.54, volume: 820000000 },
      { symbol: "FET", price: 1.72, perf24h: -24.13, volume: 910000000 },
      { symbol: "AGIX", price: 0.71, perf24h: -18.92, volume: 460000000 },
      { symbol: "OCEAN", price: 0.68, perf24h: -15.88, volume: 350000000 },
      { symbol: "AKT", price: 3.62, perf24h: -25.81, volume: 240000000 }
    ]
  },
  {
    name: "Layer 1",
    description: "BTC, ETH, SOL, ADA, AVAX, SUI.",
    rank: 77,
    index: 66.01,
    perf5m: -3.67,
    perf1h: 2.04,
    perf24h: -33.99,
    volume24h: 58000000000,
    liqUsd: 2110000000,
    liqPct: 3.65,
    longPct: 48,
    shortPct: 52,
    oiUsd: 25200000000,
    oiChange: -2.9,
    cvd: -76000000,
    tokens: [
      { symbol: "BTC", price: 64280, perf24h: -31.05, volume: 28900000000 },
      { symbol: "ETH", price: 3150, perf24h: -34.42, volume: 14900000000 },
      { symbol: "SOL", price: 142.8, perf24h: -39.18, volume: 5100000000 },
      { symbol: "ADA", price: 0.44, perf24h: -28.3, volume: 1900000000 },
      { symbol: "AVAX", price: 34.62, perf24h: -32.55, volume: 2200000000 },
      { symbol: "SUI", price: 1.23, perf24h: -28.36, volume: 950000000 }
    ]
  },
  {
    name: "DeFi",
    description: "Lending, DEX, stable issuance, staking.",
    rank: 74,
    index: 74.86,
    perf5m: -0.64,
    perf1h: 1.81,
    perf24h: -25.14,
    volume24h: 5200000000,
    liqUsd: 391000000,
    liqPct: 7.52,
    longPct: 58,
    shortPct: 42,
    oiUsd: 1720000000,
    oiChange: 3.4,
    cvd: 18000000,
    tokens: [
      { symbol: "UNI", price: 9.16, perf24h: -22.8, volume: 880000000 },
      { symbol: "AAVE", price: 92.41, perf24h: -24.21, volume: 540000000 },
      { symbol: "MKR", price: 2870, perf24h: -27.43, volume: 410000000 },
      { symbol: "ENA", price: 0.89, perf24h: -14.44, volume: 1300000000 },
      { symbol: "CRV", price: 0.39, perf24h: -31.96, volume: 620000000 },
      { symbol: "LDO", price: 1.91, perf24h: -29.02, volume: 760000000 }
    ]
  },
  {
    name: "Layer 2",
    description: "Rollups and scaling layers settling to L1s.",
    rank: 70,
    index: 79.26,
    perf5m: -0.47,
    perf1h: 0.65,
    perf24h: -20.74,
    volume24h: 3400000000,
    liqUsd: 240000000,
    liqPct: 7.07,
    longPct: 52,
    shortPct: 48,
    oiUsd: 1180000000,
    oiChange: 1.7,
    cvd: -9000000,
    tokens: [
      { symbol: "ARB", price: 1.08, perf24h: -23.12, volume: 720000000 },
      { symbol: "OP", price: 2.36, perf24h: -25.83, volume: 650000000 },
      { symbol: "MATIC", price: 0.74, perf24h: -22.9, volume: 740000000 },
      { symbol: "STRK", price: 1.31, perf24h: -28.37, volume: 390000000 },
      { symbol: "IMX", price: 2.08, perf24h: 0.66, volume: 520000000 },
      { symbol: "MANTA", price: 1.49, perf24h: -24.88, volume: 180000000 }
    ]
  },
  {
    name: "RWA",
    description: "Tokenized treasuries, credit and asset rails.",
    rank: 68,
    index: 133.73,
    perf5m: -0.13,
    perf1h: 8.74,
    perf24h: 33.73,
    volume24h: 2100000000,
    liqUsd: 54000000,
    liqPct: 2.58,
    longPct: 71,
    shortPct: 29,
    oiUsd: 610000000,
    oiChange: 15.8,
    cvd: 56000000,
    tokens: [
      { symbol: "ONDO", price: 0.94, perf24h: 42.18, volume: 620000000 },
      { symbol: "OM", price: 0.76, perf24h: 324.92, volume: 380000000 },
      { symbol: "PENDLE", price: 5.42, perf24h: 19.41, volume: 420000000 },
      { symbol: "CFG", price: 0.54, perf24h: 8.76, volume: 130000000 },
      { symbol: "POLYX", price: 0.36, perf24h: 17.22, volume: 210000000 },
      { symbol: "RIO", price: 1.48, perf24h: 12.8, volume: 160000000 }
    ]
  },
  {
    name: "Solana Apps",
    description: "SOL ecosystem apps, DEX, oracle and infra.",
    rank: 65,
    index: 86.34,
    perf5m: -0.48,
    perf1h: 5.11,
    perf24h: -13.66,
    volume24h: 4600000000,
    liqUsd: 364000000,
    liqPct: 7.91,
    longPct: 61,
    shortPct: 39,
    oiUsd: 1430000000,
    oiChange: 5.3,
    cvd: 27000000,
    tokens: [
      { symbol: "SOL", price: 142.8, perf24h: -18.08, volume: 2100000000 },
      { symbol: "JUP", price: 1.02, perf24h: -11.72, volume: 680000000 },
      { symbol: "RAY", price: 2.24, perf24h: 22.32, volume: 540000000 },
      { symbol: "PYTH", price: 0.48, perf24h: -19.34, volume: 390000000 },
      { symbol: "ORCA", price: 3.18, perf24h: -14.88, volume: 210000000 }
    ]
  },
  {
    name: "DePIN",
    description: "Wireless, storage and physical infrastructure.",
    rank: 59,
    index: 75.34,
    perf5m: 0.37,
    perf1h: 2.37,
    perf24h: -24.66,
    volume24h: 1700000000,
    liqUsd: 81000000,
    liqPct: 4.75,
    longPct: 54,
    shortPct: 46,
    oiUsd: 540000000,
    oiChange: 2.2,
    cvd: 12000000,
    tokens: [
      { symbol: "HNT", price: 5.4, perf24h: -24.3, volume: 180000000 },
      { symbol: "FIL", price: 5.88, perf24h: -28.71, volume: 520000000 },
      { symbol: "AR", price: 33.7, perf24h: -29.54, volume: 390000000 },
      { symbol: "AIOZ", price: 0.74, perf24h: -1.45, volume: 140000000 },
      { symbol: "IOTX", price: 0.052, perf24h: -31.78, volume: 120000000 },
      { symbol: "STORJ", price: 0.58, perf24h: -32.18, volume: 160000000 }
    ]
  },
  {
    name: "ETH Beta",
    description: "Ethereum native flagships and liquid staking.",
    rank: 53,
    index: 75.1,
    perf5m: -1.17,
    perf1h: 2.27,
    perf24h: -24.9,
    volume24h: 6200000000,
    liqUsd: 412000000,
    liqPct: 6.64,
    longPct: 49,
    shortPct: 51,
    oiUsd: 2310000000,
    oiChange: -1.8,
    cvd: -21000000,
    tokens: [
      { symbol: "ETH", price: 3150, perf24h: -26.31, volume: 4100000000 },
      { symbol: "LDO", price: 1.91, perf24h: -27.8, volume: 760000000 },
      { symbol: "ENS", price: 21.4, perf24h: -21.18, volume: 220000000 },
      { symbol: "ENA", price: 0.89, perf24h: -14.44, volume: 810000000 },
      { symbol: "UNI", price: 9.16, perf24h: -25.88, volume: 880000000 },
      { symbol: "MKR", price: 2870, perf24h: -33.77, volume: 410000000 }
    ]
  },
  {
    name: "GameFi",
    description: "Gaming tokens and on-chain economies.",
    rank: 47,
    index: 85.86,
    perf5m: -2.14,
    perf1h: -0.69,
    perf24h: -14.14,
    volume24h: 1400000000,
    liqUsd: 105000000,
    liqPct: 7.48,
    longPct: 46,
    shortPct: 54,
    oiUsd: 480000000,
    oiChange: -3.2,
    cvd: -16000000,
    tokens: [
      { symbol: "IMX", price: 2.08, perf24h: 0.66, volume: 520000000 },
      { symbol: "RON", price: 2.94, perf24h: 12.19, volume: 160000000 },
      { symbol: "GALA", price: 0.041, perf24h: -21.67, volume: 310000000 },
      { symbol: "AXS", price: 7.42, perf24h: -19.33, volume: 190000000 },
      { symbol: "SAND", price: 0.49, perf24h: -15.9, volume: 220000000 }
    ]
  }
];

const sectorRows = document.querySelector("#sectorRows");
const tokenRows = document.querySelector("#tokenRows");
const memberChips = document.querySelector("#memberChips");
const signalStrip = document.querySelector("#signalStrip");
const docsGrid = document.querySelector("#docsGrid");
const outlierRows = document.querySelector("#outlierRows");
const outlookAsset = document.querySelector("#outlookAsset");
const outlookSubtitle = document.querySelector("#outlookSubtitle");
const outlookConfluence = document.querySelector("#outlookConfluence");
const outlookScore = document.querySelector("#outlookScore");
const outlookStage = document.querySelector("#outlookStage");
const outlookRead = document.querySelector("#outlookRead");
const outlookLevels = document.querySelector("#outlookLevels");
const outlookEmaZones = document.querySelector("#outlookEmaZones");
const outlookConfluenceList = document.querySelector("#outlookConfluenceList");
const outlookBullish = document.querySelector("#outlookBullish");
const outlookBearish = document.querySelector("#outlookBearish");
const searchInput = document.querySelector("#searchInput");
const sortSelect = document.querySelector("#sortSelect");
const scanModeSelect = document.querySelector("#scanModeSelect");
const horizonSelect = document.querySelector("#horizonSelect");
const filterButtons = document.querySelectorAll(".filter-button");
const radarScopeButtons = document.querySelectorAll("[data-radar-scope]");
const outlierScopeLabel = document.querySelector("#outlierScopeLabel");
const snapshotTime = document.querySelector("#snapshotTime");
const snapshotStatus = document.querySelector("#snapshotStatus");
const refreshButton = document.querySelector("#refreshButton");
const appShell = document.querySelector(".desk-shell");

const API_BASE = window.QUANT_DESK_API_BASE || "http://127.0.0.1:8000/api";
const OI_HEAVY_USD = 1000000000;
const MIN_LIVE_MARKETS = 10;

const fallbackSectors = demoSectors.map((sector) => ({ ...sector, tokens: sector.tokens.map((token) => ({ ...token })) }));
let sectors = [];
let selectedOutlierSymbol = null;
let activeScanMode = "core";
let activeHorizon = "intrawick";
let activeRadarScope = "market";
let activeUniverseMeta = null;
let loadState = "idle";
let loadMessage = "Starting";
let lastScanErrors = {};
let hydrateRequestId = 0;

const metricDocs = [
  {
    title: "Index",
    formula: "avg(token_current_price / token_base_price * 100)",
    read: "Синтетическая цена сектора. Значение выше 100 означает, что equal-weighted корзина выросла от базовой точки, ниже 100 - просела.",
    source: "Считается из price data"
  },
  {
    title: "5M / 1H / 24H",
    formula: "avg(token_return_period)",
    read: "Темп движения сектора на разных таймфреймах. 5M показывает импульс, 1H - локальный тренд, 24H - дневной контекст.",
    source: "Binance, CoinGecko, CoinMarketCap"
  },
  {
    title: "Volume 24H",
    formula: "sum(token_volume_24h_usd)",
    read: "Сколько долларов проторговали участники корзины за сутки. Нужен для проверки, есть ли топливо у движения.",
    source: "Exchange / market data API"
  },
  {
    title: "LIQ %",
    formula: "liquidations_usd / volume_24h_usd * 100",
    read: "Насколько сильно ликвидации давят на сектор относительно оборота. Высокое значение часто означает forced move и повышенную волатильность.",
    source: "Coinglass, CryptoQuant, Glassnode"
  },
  {
    title: "Long / Short",
    formula: "long_liq_share / short_liq_share",
    read: "Кого сейчас сильнее выбивает. Long-heavy ликвидации чаще сопровождают резкий слив, short-heavy - squeeze вверх.",
    source: "Liquidation feeds"
  },
  {
    title: "Open Interest",
    formula: "sum(token_futures_open_interest_usd)",
    read: "Сколько денег стоит в деривативах. Рост OI означает приток плеча, падение OI - закрытие риска или ликвидационный unwind.",
    source: "Glassnode, CryptoQuant, exchanges"
  },
  {
    title: "CVD / Delta",
    formula: "market_buys_usd - market_sells_usd",
    read: "Показывает, кто агрессивнее исполняется по рынку. Плюс - покупатели бьют ask, минус - продавцы бьют bid.",
    source: "Order-flow / trades API"
  },
  {
    title: "Setup",
    formula: "rules(OI, CVD, LIQ, 24H, Long/Short)",
    read: "Человеческая метка контекста: накопление, риск squeeze, risk off, перегрев или нейтральный режим. Это не сигнал входа, а фильтр внимания.",
    source: "Derived metric"
  },
  {
    title: "Basket",
    formula: "manual sector members, equal weight",
    read: "Состав сектора. Нужен, чтобы искать лидера движения и laggards внутри той же темы.",
    source: "Manual config / taxonomy"
  }
];

const SECTOR_META = {
  Meme: {
    name: "Meme",
    description: "DOGE, SHIB, PEPE, FLOKI, BONK, WIF."
  },
  AI: {
    name: "AI",
    description: "AI infrastructure, model, compute and agent-network tokens."
  },
  RWA: {
    name: "RWA",
    description: "Tokenized treasuries, credit and asset rails."
  },
  Gaming: {
    name: "GameFi",
    description: "Gaming tokens and on-chain economies."
  },
  L2: {
    name: "Layer 2",
    description: "Rollups and scaling layers settling to L1s."
  },
  Layer1: {
    name: "Layer 1",
    description: "Base settlement layer chains."
  },
  ETH_Beta: {
    name: "ETH Beta",
    description: "Ethereum native flagships and liquid staking."
  },
  DePIN: {
    name: "DePIN",
    description: "Wireless, storage and physical infrastructure."
  },
  Payments: {
    name: "Payments",
    description: "Legacy payment chains and high-liquidity transfer networks."
  },
  DeFi: {
    name: "DeFi",
    description: "Lending, DEX, derivatives and liquidity protocols."
  },
  Oracle: {
    name: "Oracle",
    description: "Oracle networks, data feeds and market data infrastructure."
  },
  Infra: {
    name: "Infra",
    description: "General crypto infrastructure, app chains and interoperability."
  },
  Privacy_ZK: {
    name: "Privacy / ZK",
    description: "Privacy assets, zero-knowledge networks and interoperability layers."
  },
  Solana_Eco: {
    name: "Solana Eco",
    description: "Solana ecosystem apps, memes, infra and high-beta perps."
  },
  New_Listings: {
    name: "New Listings",
    description: "Fresh and thinner Binance futures listings with breakout potential."
  },
  CeFi: {
    name: "CeFi",
    description: "Exchange-linked, centralized finance and high-reflexivity perps."
  }
};

function numberOr(value, fallback = 0) {
  return typeof value === "number" && Number.isFinite(value) ? value : fallback;
}

function displayPriceForMarket(asset, marketSymbol, price) {
  const numeric = numberOr(price, null);
  if (!Number.isFinite(numeric)) return numeric;
  return marketSymbol?.startsWith(`1000${asset}`) ? numeric / 1000 : numeric;
}

function getMarketByAsset(markets) {
  return new Map(
    markets
      .filter((market) => market.exchange === "binance" && market.market_type === "futures" && market.enabled !== false)
      .map((market) => [market.asset, market])
  );
}

function calculateRank(sector, tokens) {
  const perfComponent = Math.min(Math.abs(sector.perf1h) / 5, 1) * 30;
  const volumeComponent = Math.min((sector.volumeSpike || 0) / 4, 1) * 25;
  const oiComponent = Math.min(Math.abs(sector.oiChange) / 8, 1) * 20;
  const activityComponent = Math.min(tokens.length / 6, 1) * 15;
  const cvdComponent = Math.min(Math.abs(sector.cvd) / 50000000, 1) * 10;
  return Math.round(perfComponent + volumeComponent + oiComponent + activityComponent + cvdComponent);
}

function buildLiveSectors({ universe, marketMetrics, sectorMetrics }) {
  const markets = universe.markets || [];
  const configuredSectors = universe.sectors || {};
  const marketByAsset = getMarketByAsset(markets);
  const metricBySymbol = new Map(marketMetrics.map((metric) => [metric.symbol, metric]));
  const sectorMetricByCode = new Map(sectorMetrics.map((metric) => [metric.sector, metric]));

  return Object.entries(configuredSectors)
    .map(([sectorCode, assets]) => {
      const meta = SECTOR_META[sectorCode] || { name: sectorCode, description: `${assets.join(", ")}.` };
      const sectorMetric = sectorMetricByCode.get(sectorCode) || {};
      const tokens = assets
        .map((asset) => {
          const market = marketByAsset.get(asset);
          const metric = market ? metricBySymbol.get(market.symbol) : null;
          if (!metric) {
            return null;
          }

          return {
            symbol: asset,
            marketSymbol: market?.symbol || asset,
            price: metric?.price ?? null,
            displayPrice: displayPriceForMarket(asset, market?.symbol, metric?.price),
            perf24h: numberOr(metric?.return_24h),
            volume: numberOr(metric?.quote_volume_24h, numberOr(metric?.quote_volume_5m)),
            volume5m: numberOr(metric?.quote_volume_5m),
            perf5m: numberOr(metric?.return_5m),
            perf1h: numberOr(metric?.return_1h),
            oiUsd: numberOr(metric?.oi_usd),
            oiToMcap: numberOr(metric?.oi_to_market_cap_pct),
            oiChange: numberOr(metric?.oi_change_15m),
            baseDays: metric?.base_days ?? null,
            baseHigh: metric?.base_high ?? null,
            baseLow: metric?.base_low ?? null,
            baseRange: numberOr(metric?.base_range_pct),
            baseDistance: numberOr(metric?.base_distance_to_high_pct),
            baseBreakout: numberOr(metric?.base_breakout_pct),
            baseDryUp: numberOr(metric?.base_volume_dry_up_ratio),
            basePrebreakVolume: numberOr(metric?.base_prebreak_volume_ratio),
            dailyFvgSide: metric?.daily_fvg_side || null,
            dailyFvgLow: metric?.daily_fvg_low ?? null,
            dailyFvgHigh: metric?.daily_fvg_high ?? null,
            dailyFvgAgeDays: metric?.daily_fvg_age_days ?? null,
            dailyFvgDistance: numberOr(metric?.daily_fvg_distance_pct, null),
            dailyFvgTest: metric?.daily_fvg_test ?? null,
            cvd: numberOr(metric?.cvd_15m),
            obBidWallUsd: numberOr(metric?.order_book_bid_wall_usd, null),
            obAskWallUsd: numberOr(metric?.order_book_ask_wall_usd, null),
            obImbalance: numberOr(metric?.order_book_imbalance_pct, null),
            obWallSide: metric?.order_book_wall_side || null,
            obWallDistance: numberOr(metric?.order_book_wall_distance_pct, null),
            liqPct: numberOr(metric?.liq_pct_15m),
            liqUsd: numberOr(metric?.liquidations_15m_usd),
            longLiqUsd: numberOr(metric?.long_liquidations_15m_usd),
            shortLiqUsd: numberOr(metric?.short_liquidations_15m_usd),
            volumeSpike: numberOr(metric?.volume_spike_ratio_5m),
            volumeSpike15m: numberOr(metric?.volume_spike_ratio_15m),
            consolidationRange1h: numberOr(metric?.consolidation_range_1h_pct),
            consolidationBreakout: numberOr(metric?.consolidation_breakout_pct),
            consolidationBreakoutLevel: metric?.consolidation_breakout_level ?? null,
            exchange: market?.exchange || null,
            ema4h50: metric?.ema_4h_50 ?? null,
            ema4h100: metric?.ema_4h_100 ?? null,
            ema1d50: metric?.ema_1d_50 ?? null,
            ema1d100: metric?.ema_1d_100 ?? null,
            ts: metric?.ts
          };
        })
        .filter(Boolean);

      if (!tokens.length && !sectorMetric.sector) {
        return null;
      }

      const longLiq = numberOr(sectorMetric.long_liquidations_15m_usd);
      const shortLiq = numberOr(sectorMetric.short_liquidations_15m_usd);
      const totalLiq = numberOr(sectorMetric.liquidations_15m_usd, longLiq + shortLiq);
      const longPct = totalLiq > 0 ? Math.round((longLiq / totalLiq) * 100) : 50;
      const shortPct = totalLiq > 0 ? 100 - longPct : 50;
      const obBidWallUsd = tokens.reduce((sum, token) => sum + numberOr(token.obBidWallUsd), 0);
      const obAskWallUsd = tokens.reduce((sum, token) => sum + numberOr(token.obAskWallUsd), 0);
      const obTotalWallUsd = obBidWallUsd + obAskWallUsd;
      const obImbalance = obTotalWallUsd > 0 ? ((obBidWallUsd - obAskWallUsd) / obTotalWallUsd) * 100 : null;

      const sector = {
        code: sectorCode,
        name: meta.name,
        description: meta.description,
        index: 100 + numberOr(sectorMetric.return_24h),
        perf5m: numberOr(sectorMetric.return_5m),
        perf1h: numberOr(sectorMetric.return_1h),
        perf24h: numberOr(sectorMetric.return_24h),
        volumeSpike: numberOr(sectorMetric.volume_spike_ratio_5m),
        volume5m: numberOr(sectorMetric.quote_volume_5m),
        volume24h: numberOr(sectorMetric.quote_volume_24h, tokens.reduce((sum, token) => sum + token.volume, 0)),
        liqUsd: totalLiq,
        liqPct: numberOr(sectorMetric.liq_pct_15m),
        longPct,
        shortPct,
        oiUsd: numberOr(sectorMetric.oi_usd, tokens.reduce((sum, token) => sum + token.oiUsd, 0)),
        oiChange: numberOr(sectorMetric.oi_change_15m),
        cvd: numberOr(sectorMetric.cvd_15m),
        obBidWallUsd,
        obAskWallUsd,
        obImbalance,
        obWallSide: obImbalance === null ? null : obImbalance >= 0 ? "bid" : "ask",
        activeMemberRatio: numberOr(sectorMetric.active_member_ratio, tokens.length / Math.max(assets.length, 1)),
        ts: sectorMetric.ts || tokens.find((token) => token.ts)?.ts,
        tokens
      };

      return { ...sector, rank: calculateRank(sector, tokens) };
    })
    .filter(Boolean);
}

async function fetchJson(path, options = {}) {
  const { timeoutMs = 4500, ...fetchOptions } = options;
  const controller = new AbortController();
  let timeoutId;
  const timeoutError = new Promise((_, reject) => {
    timeoutId = window.setTimeout(() => {
      controller.abort();
      reject(new Error(`${path} timed out after ${timeoutMs}ms`));
    }, timeoutMs);
  });

  let response;
  try {
    response = await Promise.race([
      fetch(`${API_BASE}${path}`, {
        cache: "no-store",
        ...fetchOptions,
        signal: controller.signal
      }),
      timeoutError
    ]);
  } finally {
    if (timeoutId) {
      window.clearTimeout(timeoutId);
    }
  }

  if (!response.ok) {
    throw new Error(`${response.status} ${response.statusText}`);
  }
  return response.json();
}

async function loadApiPayload(mode = "core") {
  const modeQuery = `?mode=${encodeURIComponent(mode)}`;
  const universe = await fetchJson(`/config/universe${modeQuery}`, { timeoutMs: mode === "core" ? 15000 : 45000 });
  try {
    const preview = await fetchJson(`/ingestion/binance/preview${modeQuery}`, { method: "POST", timeoutMs: mode === "full" ? 240000 : 180000 });
    if ((preview.market_metrics?.length || 0) < MIN_LIVE_MARKETS || !preview.sector_metrics?.length) {
      throw new Error(`empty preview metrics; errors=${Object.keys(preview.errors || {}).length}`);
    }
    return {
      universe: preview.universe || universe,
      marketMetrics: preview.market_metrics,
      sectorMetrics: preview.sector_metrics,
      events: preview.events,
      errors: preview.errors || {},
      source: "live"
    };
  } catch (error) {
    console.info("Quant Desk scan metrics unavailable:", error);
  }

  if (mode !== "core") {
    return {
      universe,
      marketMetrics: [],
      sectorMetrics: [],
      events: []
    };
  }

  try {
    const [marketMetrics, sectorMetrics, events] = await Promise.all([
      fetchJson("/metrics/latest", { timeoutMs: 3000 }),
      fetchJson("/sectors/latest", { timeoutMs: 3000 }),
      fetchJson("/events", { timeoutMs: 3000 })
    ]);

    if (marketMetrics.length && sectorMetrics.length) {
      return { universe, marketMetrics, sectorMetrics, events, errors: {}, source: "latest" };
    }
  } catch (error) {
    console.info("Quant Desk latest metrics unavailable:", error);
  }

  const cached = await fetchJson("/cache/latest-preview", { timeoutMs: 8000 });
  return {
    universe: cached.universe || universe,
    marketMetrics: cached.market_metrics || [],
    sectorMetrics: cached.sector_metrics || [],
    events: cached.events || [],
    errors: cached.errors || {},
    source: "cache"
  };
}

async function loadCachedPayload() {
  const cached = await fetchJson("/cache/latest-preview", { timeoutMs: 5000 });
  return {
    universe: cached.universe || null,
    marketMetrics: cached.market_metrics || [],
    sectorMetrics: cached.sector_metrics || [],
    events: cached.events || [],
    errors: cached.errors || {},
    source: "cache"
  };
}

function latestTimestamp(items) {
  const timestamps = items
    .map((item) => Date.parse(item.ts))
    .filter((value) => Number.isFinite(value));

  if (!timestamps.length) return null;
  return new Date(Math.max(...timestamps));
}

function setLoadState(state, message = "") {
  loadState = state;
  loadMessage = message;
  if (appShell) {
    appShell.dataset.state = state;
  }
  if (snapshotStatus) {
    snapshotStatus.textContent = message;
  }
  if (refreshButton) {
    refreshButton.disabled = state === "loading";
    refreshButton.textContent = state === "loading" ? "Scanning" : "Refresh";
  }
}

function renderSnapshotTime(date, label = "") {
  if (!snapshotTime) return;
  if (!date) {
    snapshotTime.textContent = label || "Demo";
    return;
  }

  const time = date.toLocaleTimeString("en-GB", {
    hour: "2-digit",
    minute: "2-digit",
    timeZone: "UTC"
  });
  snapshotTime.textContent = `${label}${time} UTC`;
}

function hasOrderBookMetrics(marketMetrics) {
  return marketMetrics.some((metric) => Number.isFinite(metric?.order_book_imbalance_pct));
}

function applyHydratedPayload(payload, previousSelectedName, previousSelectedOutlier, mode, options = {}) {
  if (payload.source !== "cache" && (payload.marketMetrics.length < MIN_LIVE_MARKETS || !payload.sectorMetrics.length)) {
    throw new Error("empty live metrics");
  }

  const liveSectors = buildLiveSectors(payload);
  if (!liveSectors.length) {
    throw new Error("empty live payload");
  }

  sectors = liveSectors;
  activeUniverseMeta = payload.universe || null;
  lastScanErrors = payload.errors || {};
  selectedName = sectors.some((sector) => sector.name === previousSelectedName) ? previousSelectedName : sectors[0].name;
  selectedOutlierSymbol = previousSelectedOutlier;

  const scanCount = payload.universe?.scan_deep_markets;
  const modeLabel = payload.source === "cache"
    ? "Cached "
    : payload.universe?.scan_unavailable
    ? "Limited "
    : mode === "full" ? `Full ${scanCount || ""} ` : mode === "expanded" ? `Expanded ${scanCount || ""} ` : "Live ";
  renderSnapshotTime(latestTimestamp(payload.sectorMetrics), payload.marketMetrics.length ? modeLabel : `${modeLabel}pairs`);

  const skippedCount = Object.keys(lastScanErrors).length;
  if (payload.source === "cache") {
    setLoadState("cache", options.refreshing ? `${payload.marketMetrics.length} cached pairs, refreshing` : `${payload.marketMetrics.length} cached pairs`);
  } else {
    setLoadState("live", skippedCount ? `Live, ${skippedCount} skipped` : `${payload.marketMetrics.length} pairs live`);
  }

  renderSignals();
  renderRows();
  renderOutlierRadar();
}

async function hydrateFromApi() {
  const mode = activeScanMode;
  const requestId = ++hydrateRequestId;
  const previousSelectedName = selectedName;
  const previousSelectedOutlier = selectedOutlierSymbol;
  setLoadState("loading", mode === "full" ? "Full market scan" : mode === "expanded" ? "Expanded scan" : "Live scan");
  renderSnapshotTime(null, mode === "full" ? "Full scan" : mode === "expanded" ? "Expanded" : "Loading");
  renderSignals();
  renderRows();
  renderOutlierRadar();

  let renderedFallback = false;
  if (mode === "core") {
    try {
      const cachedPayload = await loadCachedPayload();
      if (requestId !== hydrateRequestId) return;
      applyHydratedPayload(cachedPayload, previousSelectedName, previousSelectedOutlier, mode, { refreshing: true });
      renderedFallback = true;
    } catch (error) {
      console.info("Quant Desk cached preview unavailable:", error);
    }
  }

  try {
    let payload = await loadApiPayload(mode);
    if (requestId !== hydrateRequestId) return;

    const needsPreview =
      payload.marketMetrics.length < MIN_LIVE_MARKETS ||
      !payload.sectorMetrics.length ||
      (payload.source !== "cache" && !hasOrderBookMetrics(payload.marketMetrics));

    if (needsPreview) {
      renderSnapshotTime(null, "Previewing");
      const preview = await fetchJson(`/ingestion/binance/preview?mode=${encodeURIComponent(mode)}`, { method: "POST", timeoutMs: mode === "full" ? 240000 : 180000 });
      if (requestId !== hydrateRequestId) return;
      payload = {
        universe: preview.universe || payload.universe,
        marketMetrics: preview.market_metrics,
        sectorMetrics: preview.sector_metrics,
        events: preview.events,
        errors: preview.errors || {},
        source: "live"
      };
    }

    applyHydratedPayload(payload, previousSelectedName, previousSelectedOutlier, mode);
  } catch (error) {
    if (requestId !== hydrateRequestId) return;
    if (renderedFallback) {
      setLoadState("cache", `${sectors.flatMap((sector) => sector.tokens).length} cached pairs, live unavailable`);
      console.info("Quant Desk live refresh unavailable:", error);
      return;
    }
    sectors = [];
    activeUniverseMeta = null;
    lastScanErrors = {};
    selectedName = null;
    selectedOutlierSymbol = previousSelectedOutlier;
    renderSnapshotTime(null, "Unavailable");
    setLoadState("error", "API unavailable");
    console.info("Quant Desk API unavailable:", error);
  }

  renderSignals();
  renderRows();
  renderOutlierRadar();
}

let selectedName = null;
let activeFilter = "all";

function signedClass(value) {
  return numberOr(value) < 0 ? "value-negative" : "value-positive";
}

function formatPct(value) {
  const numeric = numberOr(value);
  return `${numeric > 0 ? "+" : ""}${numeric.toFixed(2)}%`;
}

function formatMoney(value) {
  const numeric = numberOr(value);
  const abs = Math.abs(numeric);
  const sign = numeric < 0 ? "-" : numeric > 0 ? "+" : "";

  if (abs >= 1000000000) {
    return `${sign}$${(abs / 1000000000).toFixed(1)}B`;
  }

  if (abs >= 1000000) {
    return `${sign}$${(abs / 1000000).toFixed(0)}M`;
  }

  return `${sign}$${abs.toFixed(0)}`;
}

function formatOrderBookPressure(value) {
  if (!Number.isFinite(value)) return "waiting";
  const side = value >= 0 ? "bid" : "ask";
  return `${side} ${formatPct(Math.abs(value)).replace("+", "")}`;
}

function getSignal(sector) {
  const setup = getSetup(sector);
  const oiChange = numberOr(sector.oiChange);
  const cvd = numberOr(sector.cvd);
  const perf5m = numberOr(sector.perf5m);
  const perf1h = numberOr(sector.perf1h);
  const longPct = numberOr(sector.longPct, 50);
  const shortPct = numberOr(sector.shortPct, 50);

  if (
    ["setup-bid", "setup-accumulation"].includes(setup.className) ||
    (oiChange > 0.75 && cvd > 0 && perf5m >= -0.8) ||
    (cvd > 0 && perf1h > 0 && longPct >= shortPct)
  ) {
    return { side: "long", label: "LONG", symbol: "▲", className: "signal-long" };
  }

  if (
    ["setup-risk", "setup-exhaustion"].includes(setup.className) ||
    (oiChange < -0.75 && cvd < 0) ||
    (cvd < 0 && perf1h < 0 && shortPct >= longPct)
  ) {
    return { side: "short", label: "SHORT", symbol: "▼", className: "signal-short" };
  }

  return { side: "unclear", label: "UNCLEAR", symbol: "△", className: "signal-unclear" };
}

function getSectorExchanges(sector) {
  const exchangeCodes = {
    binance: "BNB",
    bybit: "BYB",
    okx: "OKX"
  };

  const exchanges = [
    ...new Set(
      (sector.tokens || [])
        .map((token) => (token.exchange || "").toLowerCase())
        .filter(Boolean)
        .map((exchange) => exchangeCodes[exchange] || exchange.slice(0, 3).toUpperCase())
    )
  ];

  return exchanges.length ? exchanges.slice(0, 3) : ["BNB", "BYB"];
}

function getPairLongShort(token, sector) {
  const longLiq = numberOr(token.longLiqUsd);
  const shortLiq = numberOr(token.shortLiqUsd);
  const totalLiq = numberOr(token.liqUsd, longLiq + shortLiq);

  if (totalLiq > 0 && (longLiq > 0 || shortLiq > 0)) {
    const longPct = Math.round((longLiq / totalLiq) * 100);
    return {
      longPct: Math.max(0, Math.min(longPct, 100)),
      shortPct: Math.max(0, Math.min(100 - longPct, 100)),
      source: "pair"
    };
  }

  const cvd = numberOr(token.cvd);
  const oiChange = numberOr(token.oiChange);
  const perf1h = numberOr(token.perf1h, numberOr(sector.perf1h));
  const bias = Math.max(-18, Math.min(18, cvd / 2000000 + oiChange * 1.7 + perf1h * 1.2));
  const sectorLong = numberOr(sector.longPct, 50);
  const longPct = Math.round(Math.max(15, Math.min(85, sectorLong + bias)));

  return {
    longPct,
    shortPct: 100 - longPct,
    source: "derived"
  };
}

function getPairSignal(token, sector) {
  const flow = getPairLongShort(token, sector);
  const cvd = numberOr(token.cvd, numberOr(sector.cvd));
  const oiChange = numberOr(token.oiChange, numberOr(sector.oiChange));
  const perf5m = numberOr(token.perf5m, numberOr(sector.perf5m));
  const perf1h = numberOr(token.perf1h, numberOr(sector.perf1h));

  if ((cvd > 0 && oiChange > 0.25 && perf5m >= -0.6) || (flow.longPct >= 58 && perf1h > 0)) {
    return { side: "long", label: "LONG", symbol: "▲", className: "signal-long" };
  }

  if ((cvd < 0 && oiChange < -0.25) || (flow.shortPct >= 58 && perf1h < 0)) {
    return { side: "short", label: "SHORT", symbol: "▼", className: "signal-short" };
  }

  return { side: "unclear", label: "WAIT", symbol: "△", className: "signal-unclear" };
}

function volumeTo24hPct(volume5m, volume24h) {
  if (!Number.isFinite(volume5m) || !Number.isFinite(volume24h) || volume24h <= 0) return 0;
  return (volume5m / volume24h) * 100;
}

function estimateVolume5m(token, sector) {
  const liveVolume = numberOr(token.volume5m);
  if (liveVolume > 0) return liveVolume;
  const expectedFiveMinuteShare = 1 / 288;
  const spike = numberOr(token.volumeSpike, numberOr(sector.volumeSpike, 1));
  return numberOr(token.volume) * expectedFiveMinuteShare * Math.max(spike, 0.25);
}

function formatVolumeRatio(value) {
  const numeric = numberOr(value);
  if (numeric >= 10) return `${numeric.toFixed(1)}%`;
  if (numeric >= 1) return `${numeric.toFixed(2)}%`;
  return `${numeric.toFixed(3)}%`;
}

function formatPrice(value) {
  if (value === null || value === undefined || Number.isNaN(value)) return "-";
  if (value >= 1000) return `$${value.toLocaleString("en-US", { maximumFractionDigits: 0 })}`;
  if (value >= 1) return `$${value.toFixed(2)}`;
  if (value >= 0.01) return `$${value.toFixed(3)}`;
  return `$${value.toPrecision(2)}`;
}

function formatLevel(value) {
  if (!Number.isFinite(value) || value <= 0) return "-";
  if (value >= 1000) return `$${value.toLocaleString("en-US", { maximumFractionDigits: 0 })}`;
  if (value >= 1) return `$${value.toFixed(3)}`;
  if (value >= 0.01) return `$${value.toFixed(4)}`;
  return `$${value.toPrecision(3)}`;
}

function getSetup(sector) {
  const perf1h = numberOr(sector.perf1h);
  const perf24h = numberOr(sector.perf24h);
  const liqPct = numberOr(sector.liqPct);
  const oiChange = numberOr(sector.oiChange);
  const cvd = numberOr(sector.cvd);
  const longPct = numberOr(sector.longPct, 50);
  const shortPct = numberOr(sector.shortPct, 50);
  const skew = Math.abs(longPct - shortPct);
  const isStableShortTerm = Math.abs(perf1h) < 1.2;

  if (liqPct >= 10) {
    return {
      label: "Squeeze Risk",
      className: "setup-squeeze",
      score: 95,
      confidence: "высокая уверенность",
      reason: "LIQ pressure экстремальный. Движение похоже на forced move, поэтому волатильность может оставаться грязной до сброса плеча."
    };
  }

  if (perf24h > 25 && oiChange > 8) {
    return {
      label: "Exhaustion Watch",
      className: "setup-exhaustion",
      score: 82,
      confidence: "средняя уверенность",
      reason: "Сектор уже сильно вытянут, а OI продолжает расти. Перед догоняющим входом стоит ждать затухания объема или разворота CVD."
    };
  }

  if (perf24h < 0 && oiChange < 0 && cvd < 0) {
    return {
      label: "Risk Off",
      className: "setup-risk",
      score: 78,
      confidence: "высокая уверенность",
      reason: "Цена падает, CVD отрицательный, OI сокращается. Обычно это означает, что риск из сектора выходит."
    };
  }

  if (perf24h < 0 && oiChange > 3 && cvd > 0 && liqPct < 8) {
    return {
      label: "Lagging Bid",
      className: "setup-bid",
      score: 74,
      confidence: "средняя уверенность",
      reason: "Сектор все еще красный по 24H, но OI и CVD уже положительные. Покупатели могут набирать позицию до подтверждения ценой."
    };
  }

  if (cvd < 0 && oiChange > 0 && isStableShortTerm) {
    return {
      label: "Absorption",
      className: "setup-absorption",
      score: 69,
      confidence: "средняя уверенность",
      reason: "Рыночные продажи проходят по ленте, но краткосрочная цена держится. Это может означать, что лимитный покупатель поглощает предложение."
    };
  }

  if (oiChange > 4 && liqPct < 7 && cvd > 0) {
    return {
      label: "Accumulation",
      className: "setup-accumulation",
      score: 66,
      confidence: "средняя уверенность",
      reason: "OI растет вместе с положительным CVD, а ликвидационное давление умеренное. Это чище, чем импульс на одних ликвидациях."
    };
  }

  if (skew >= 20 && liqPct >= 7) {
    return {
      label: "Crowded Side",
      className: "setup-squeeze",
      score: 61,
      confidence: "низкая уверенность",
      reason: "Позиционирование заметно перекошено, а ликвидации повышены. В такой зоне часто идут шумные движения вокруг стопов."
    };
  }

  if ((oiChange < -0.5 && cvd < 0) || (cvd < 0 && perf1h < 0 && shortPct >= longPct)) {
    return {
      label: "Short Flow",
      className: "setup-risk",
      score: 58,
      confidence: "средняя уверенность",
      reason: "Directional read bearish: CVD/TCD в минусе, локальный импульс слабый, а OI не дает чистого бычьего подтверждения. Это не полный risk-off, но flow bias вниз."
    };
  }

  if ((oiChange > 0.5 && cvd > 0) || (cvd > 0 && perf1h > 0 && longPct >= shortPct)) {
    return {
      label: "Long Flow",
      className: "setup-bid",
      score: 58,
      confidence: "средняя уверенность",
      reason: "Directional read bullish: CVD/TCD в плюсе, локальный импульс держится, и покупатель начинает забирать ленту. Это еще не полное накопление, но flow bias вверх."
    };
  }

  return {
    label: "Neutral Flow",
    className: "setup-neutral",
    score: 45,
    confidence: "низкая уверенность",
    reason: "У сектора пока нет чистого перекоса. Лучше ждать, пока OI, CVD или LIQ подтвердят более сильный контекст."
  };
}

function getFilteredSectors() {
  const query = searchInput.value.trim().toLowerCase();

  return sectors
    .filter((sector) => {
      const tokenHit = sector.tokens.some((token) => {
        const symbol = token.symbol.toLowerCase();
        return query.length <= 2 ? symbol === query : symbol.includes(query);
      });
      const nameHit = sector.name.toLowerCase().includes(query);
      const codeHit = (sector.code || "").toLowerCase().includes(query);
      const descriptionHit = query.length >= 3 && sector.description.toLowerCase().includes(query);
      const textHit = nameHit || codeHit || descriptionHit;
      const queryPass = !query || textHit || tokenHit;

      if (!queryPass) return false;
      if (activeFilter === "long") return getSignal(sector).side === "long";
      if (activeFilter === "short") return getSignal(sector).side === "short";
      if (activeFilter === "unclear") return getSignal(sector).side === "unclear";
      if (activeFilter === "oi-heavy") return numberOr(sector.oiUsd) >= OI_HEAVY_USD;

      return true;
    })
    .sort((a, b) => {
      if (sortSelect.value === "setupScore") return getSetup(b).score - getSetup(a).score;
      return numberOr(b[sortSelect.value]) - numberOr(a[sortSelect.value]);
    });
}

function renderSignals() {
  if (!sectors.length) {
    const label = loadState === "loading" ? "Scanning" : "No data";
    signalStrip.innerHTML = [
      ["Status", label, "neutral"],
      ["Mode", activeScanMode, "oi"],
      ["Horizon", activeHorizon, "oi"],
      ["Sectors", "-", "neutral"],
      ["Pairs", "-", "neutral"],
      ["Source", loadState, "unclear"]
    ]
      .map(
        ([cardLabel, value, tone]) => `
          <div class="signal-card signal-card-${tone}">
            <span>${cardLabel}</span>
            <strong>${value}</strong>
          </div>
        `
      )
      .join("");
    return;
  }

  const signals = sectors.map(getSignal);
  const longCount = signals.filter((signal) => signal.side === "long").length;
  const shortCount = signals.filter((signal) => signal.side === "short").length;
  const unclearCount = signals.filter((signal) => signal.side === "unclear").length;
  const oiHeavyCount = sectors.filter((sector) => numberOr(sector.oiUsd) >= OI_HEAVY_USD).length;
  const pairCount = sectors.reduce((sum, sector) => sum + sector.tokens.length, 0);
  const totalPerps = activeUniverseMeta?.scan_total_binance_usdt_perps;
  const pairLabel = totalPerps ? `Pairs / ${totalPerps}` : "Pairs";

  signalStrip.innerHTML = [
    ["Total sectors", sectors.length, "neutral"],
    [pairLabel, pairCount, "oi"],
    ["Long", longCount, "long"],
    ["Short", shortCount, "short"],
    ["Unclear", unclearCount, "unclear"],
    ["OI >$1B", oiHeavyCount, "oi"]
  ]
    .map(
      ([label, value, tone]) => `
        <div class="signal-card signal-card-${tone}">
          <span>${label}</span>
          <strong>${value}</strong>
        </div>
      `
    )
    .join("");
}

function marketAverage(metric) {
  const values = sectors.map((sector) => numberOr(sector[metric], null)).filter((value) => value !== null);
  if (!values.length) return 0;
  return values.reduce((sum, value) => sum + value, 0) / values.length;
}

function clampScore(value, maxValue, weight) {
  return Math.min(Math.max(value, 0) / maxValue, 1) * weight;
}

function getFlowIntensityPct(flowUsd, volume24h) {
  const volume = numberOr(volume24h);
  if (volume <= 0) return 0;
  return (numberOr(flowUsd) / volume) * 100;
}

function getOrderBookSupportScore(candidate) {
  if (!Number.isFinite(candidate.obImbalance)) return 0;
  const directional = candidate.perf1h >= 0 ? candidate.obImbalance : -candidate.obImbalance;
  return directional;
}

function getEmaTrendCount(candidate) {
  return [
    candidate.ema4h50,
    candidate.ema4h100,
    candidate.ema1d50,
    candidate.ema1d100
  ].filter((level) => Number.isFinite(level) && level > 0 && candidate.price > level).length;
}

function getMediumTermScore(candidate) {
  return Math.round(
    clampScore(candidate.baseScore, 100, 26) +
      clampScore(candidate.baseDays, 20, 8) +
      clampScore(candidate.baseDistance + 9, 10.5, 12) +
      clampScore(candidate.baseBreakout + 0.35, 2.6, 14) +
      clampScore(candidate.basePrebreakVolume - 0.85, 2.8, 8) +
      clampScore(candidate.rs24h + 1.5, 16, 13) +
      clampScore(candidate.marketRs, 22, 10) +
      clampScore(candidate.oiToMcap, 4, 10) +
      clampScore(candidate.oiChange, 6, 8) +
      clampScore(candidate.volumeTo24h, 1.2, 5) +
      clampScore(candidate.flowUsd, 50000000, 4) +
      clampScore(candidate.flowIntensity + 0.05, 0.45, 10) +
      clampScore(getOrderBookSupportScore(candidate) + 10, 45, 8) +
      clampScore(candidate.emaTrend, 4, 12)
  );
}

function getOutlierStage(candidate) {
  if (activeHorizon === "intrawick") {
    if (
      candidate.baseBreakout >= 15 ||
      candidate.rs24h >= 35 ||
      (candidate.perf24h >= 45 && candidate.volumeSpike15m >= 3)
    ) {
      return {
        label: "Extended Breakout",
        className: "stage-risk",
        read: "Base already expanded hard; wait for retest, reset, or fresh accumulation."
      };
    }

    if (
      candidate.mediumScore >= 74 &&
      (candidate.baseBreakout >= 0.1 || candidate.baseDistance >= -1.5) &&
      candidate.emaTrend >= 2 &&
      (candidate.basePrebreakVolume >= 0.9 || candidate.oiToMcap >= 0.8 || candidate.oiChange > 0)
    ) {
      return {
        label: "Intrawick Breakout",
        className: "stage-base",
        read: "Multi-day base is resolving with 4H/1D support, OI and TCD/CVD confirmation."
      };
    }

    if (
      candidate.mediumScore >= 68 &&
      candidate.baseDays >= 8 &&
      candidate.baseDistance >= -6 &&
      candidate.flowIntensity > 0.08 &&
      candidate.oiChange >= 0
    ) {
      return {
        label: "TCD Build",
        className: "stage-accumulation",
        read: "Positive taker flow is appearing inside the base before full price expansion."
      };
    }

    if (candidate.mediumScore >= 64 && candidate.baseDays >= 8 && candidate.baseDistance >= -7 && candidate.emaTrend >= 2) {
      return {
        label: "Intrawick Build",
        className: "stage-accumulation",
        read: "Base is mature; watch volume and TCD/CVD expansion before the clean breakout."
      };
    }

    if (candidate.mediumScore >= 58 && candidate.emaTrend >= 3 && candidate.rs24h > 0) {
      return {
        label: "Trend Continuation",
        className: "stage-expansion",
        read: "Price is holding above key 4H/1D EMA zones with relative strength."
      };
    }

    if (candidate.baseScore >= 50 && (candidate.oiChange > 0 || candidate.flowUsd > 0 || candidate.oiToMcap >= 0.8)) {
      return {
        label: "Base Accumulation",
        className: "stage-watch",
        read: "Base exists and positioning is improving, but breakout pressure is not complete yet."
      };
    }
  }

  if (
    candidate.baseBreakout >= 0.2 &&
    candidate.basePrebreakVolume >= 1.2 &&
    (candidate.oiChange > 0 || candidate.oiToMcap >= 0.8)
  ) {
    return {
      label: "Base Breakout",
      className: "stage-base",
      read: "Multi-day base is breaking with volume/OI support."
    };
  }

  if (candidate.breakoutScore >= 72) {
    return {
      label: "Box Breakout",
      className: "stage-breakout",
      read: "Compression is breaking with volume/OI confirmation."
    };
  }

  if (candidate.boxRange > 0 && candidate.boxRange <= 2.4 && candidate.breakoutPct > -0.25 && candidate.volumeSpike15m > 1.2) {
    return {
      label: "Breakout Watch",
      className: "stage-outlier",
      read: "Price is pressing the box high; needs a close through the level."
    };
  }

  if (candidate.volumeSpike15m >= 2 && candidate.oiChange > 1 && candidate.perf1h > 0) {
    return {
      label: "Volume Build",
      className: "stage-accumulation",
      read: "Volume and OI are building before a clean range break."
    };
  }

  if (candidate.baseScore >= 65) {
    return {
      label: "Base Build",
      className: "stage-accumulation",
      read: "Long base is active; volume or OI is starting to expand."
    };
  }

  if (candidate.baseScore >= 50) {
    return {
      label: "Long Base Watch",
      className: "stage-watch",
      read: "Multi-day base is close enough to monitor for the first expansion."
    };
  }

  if (candidate.score >= 78 && candidate.rs1h > 1.5 && candidate.flowUsd > 0) {
    return {
      label: "Early Outlier",
      className: "stage-outlier",
      read: "Asset is already detaching from its sector with flow support."
    };
  }

  if (candidate.score >= 70 && candidate.oiChange > 3 && candidate.flowUsd > 0) {
    return {
      label: "Accumulation",
      className: "stage-accumulation",
      read: "OI and flow are building before full price expansion."
    };
  }

  if (candidate.rs24h > 12 && candidate.oiChange > 7) {
    return {
      label: "Expansion",
      className: "stage-expansion",
      read: "Momentum is active; watch funding and liquidation risk."
    };
  }

  if (candidate.liqPct >= 7 || candidate.rs24h > 24) {
    return {
      label: "Exhaustion Risk",
      className: "stage-risk",
      read: "Move is hot; late entries need tighter confirmation."
    };
  }

  return {
    label: "Watchlist",
    className: "stage-watch",
    read: "Some ingredients are present, but confirmation is incomplete."
  };
}

function getSelectedSectorForRadar() {
  if (activeRadarScope !== "sector" || !selectedName) return null;
  return sectors.find((sector) => sector.name === selectedName) || null;
}

function buildOutlierCandidates() {
  const market24h = marketAverage("perf24h");
  const seen = new Map();
  const selectedSector = getSelectedSectorForRadar();
  const sourceSectors = selectedSector ? [selectedSector] : sectors;

  sourceSectors.forEach((sector) => {
    sector.tokens.forEach((token) => {
      const perf1h = numberOr(token.perf1h, numberOr(sector.perf1h));
      const perf24h = numberOr(token.perf24h);
      const rs1h = perf1h - numberOr(sector.perf1h);
      const rs24h = perf24h - numberOr(sector.perf24h);
      const marketRs = perf24h - market24h;
      const oiChange = numberOr(token.oiChange, numberOr(sector.oiChange));
      const oiToMcap = numberOr(token.oiToMcap);
      const flowUsd = numberOr(token.cvd, numberOr(sector.cvd));
      const flowIntensity = getFlowIntensityPct(flowUsd, numberOr(token.volume));
      const obBidWallUsd = numberOr(token.obBidWallUsd, null);
      const obAskWallUsd = numberOr(token.obAskWallUsd, null);
      const obImbalance = numberOr(token.obImbalance, null);
      const obWallDistance = numberOr(token.obWallDistance, null);
      const liqPct = numberOr(token.liqPct, numberOr(sector.liqPct));
      const volumeSpike = numberOr(token.volumeSpike, numberOr(sector.volumeSpike, 1));
      const volumeSpike15m = numberOr(token.volumeSpike15m, volumeSpike);
      const boxRange = numberOr(token.consolidationRange1h);
      const breakoutPct = numberOr(token.consolidationBreakout);
      const price = numberOr(token.price);
      const volumeShare = sector.volume24h > 0 ? numberOr(token.volume) / sector.volume24h : 0;
      const volume5m = estimateVolume5m(token, sector);
      const volumeTo24h = volumeTo24hPct(volume5m, numberOr(token.volume));
      const isCompressed = boxRange > 0 && boxRange <= 3.2;
      const isBreakingBox = breakoutPct >= 0.18;
      const baseDays = numberOr(token.baseDays);
      const baseRange = numberOr(token.baseRange);
      const baseDistance = numberOr(token.baseDistance);
      const baseBreakout = numberOr(token.baseBreakout);
      const baseDryUp = numberOr(token.baseDryUp);
      const basePrebreakVolume = numberOr(token.basePrebreakVolume);
      const breakoutScore = Math.round(
        (boxRange > 0 ? clampScore(3.2 - boxRange, 3.2, 18) : 0) +
          clampScore(breakoutPct, 1.5, 24) +
          clampScore(volumeSpike15m - 1, 3, 22) +
          clampScore(oiChange, 4, 18) +
          clampScore(perf1h, 3, 10) +
          (isCompressed && isBreakingBox ? 8 : 0)
      );
      const baseScore = Math.round(
        clampScore(baseDays, 20, 12) +
          (baseRange > 0 ? clampScore(38 - baseRange, 38, 12) : 0) +
          clampScore(baseDistance + 8, 9.5, 18) +
          clampScore(baseBreakout + 0.5, 3, 20) +
          clampScore(1.05 - baseDryUp, 1.05, 10) +
          clampScore(basePrebreakVolume - 0.9, 2.6, 16) +
          clampScore(oiChange, 5, 8) +
          clampScore(oiToMcap, 4, 4)
      );

      const emaTrend = getEmaTrendCount({
        price,
        ema4h50: token.ema4h50,
        ema4h100: token.ema4h100,
        ema1d50: token.ema1d50,
        ema1d100: token.ema1d100
      });
      const mediumScore = getMediumTermScore({
        price,
        perf24h,
        marketRs,
        volumeTo24h,
        baseDays,
        baseDistance,
        baseBreakout,
        basePrebreakVolume,
        baseScore,
        oiToMcap,
        emaTrend,
        rs24h,
        oiChange,
        flowUsd,
        flowIntensity,
        obImbalance,
        perf1h
      });
      const intradayScore = Math.round(
        clampScore(rs1h + 0.5, 4, 22) +
          clampScore(rs24h + 1, 18, 22) +
          clampScore(marketRs, 24, 14) +
          clampScore(volumeSpike - 1, 3, 14) +
          clampScore(volumeTo24h, 1.2, 10) +
          clampScore(oiChange, 8, 10) +
          clampScore(oiToMcap, 5, 5) +
          clampScore(flowUsd, 50000000, 8) +
          clampScore(breakoutScore, 100, 12) +
          clampScore(baseScore, 100, 18)
      );
      const score = activeHorizon === "intrawick" ? mediumScore : intradayScore;

      const candidate = {
        symbol: token.symbol,
        sector: sector.name,
        price,
        displayPrice: token.displayPrice ?? price,
        perf1h,
        perf24h,
        marketRs,
        volumeShare,
        volume5m,
        volumeTo24h,
        volumeSpike,
        volumeSpike15m,
        boxRange,
        breakoutPct,
        breakoutScore,
        breakoutLevel: token.consolidationBreakoutLevel,
        baseDays,
        baseHigh: token.baseHigh,
        baseLow: token.baseLow,
        baseRange,
        baseDistance,
        baseBreakout,
        baseDryUp,
        basePrebreakVolume,
        baseScore,
        dailyFvgSide: token.dailyFvgSide,
        dailyFvgLow: token.dailyFvgLow,
        dailyFvgHigh: token.dailyFvgHigh,
        dailyFvgAgeDays: token.dailyFvgAgeDays,
        dailyFvgDistance: token.dailyFvgDistance,
        dailyFvgTest: token.dailyFvgTest,
        mediumScore,
        intradayScore,
        oiToMcap,
        ema4h50: token.ema4h50,
        ema4h100: token.ema4h100,
        ema1d50: token.ema1d50,
        ema1d100: token.ema1d100,
        emaTrend,
        score,
        rs1h,
        rs24h,
        oiChange,
        flowUsd,
        flowIntensity,
        obBidWallUsd,
        obAskWallUsd,
        obImbalance,
        obWallSide: token.obWallSide,
        obWallDistance,
        liqPct
      };
      const stage = getOutlierStage(candidate);
      const previous = seen.get(candidate.symbol);
      if (!previous || candidate.score > previous.score) {
        seen.set(candidate.symbol, { ...candidate, ...stage });
      }
    });
  });

  const ranked = [...seen.values()].sort((a, b) => b.score - a.score);
  const active = ranked.filter((candidate) => {
    if (activeHorizon === "intrawick") {
      return candidate.mediumScore >= 42 || candidate.baseScore >= 45 || candidate.emaTrend >= 3 || candidate.oiToMcap >= 0.8 || candidate.flowIntensity > 0.08;
    }
    return candidate.score >= 35 || candidate.rs24h > 3 || candidate.rs1h > 1 || candidate.breakoutScore >= 55 || candidate.baseScore >= 45;
  });
  const limit = activeScanMode === "full" ? 40 : activeScanMode === "expanded" ? 28 : 10;
  return (active.length >= limit ? active : ranked).slice(0, limit);
}

function renderOutlierRadar() {
  if (!outlierRows) return;
  const candidates = buildOutlierCandidates();
  const selectedSector = getSelectedSectorForRadar();
  if (outlierScopeLabel) {
    outlierScopeLabel.textContent = selectedSector
      ? `${selectedSector.name} only · intrawick base + TCD/CVD + OI/MCAP`
      : "all market · intrawick base + TCD/CVD + OI/MCAP";
  }
  radarScopeButtons.forEach((button) => {
    button.classList.toggle("is-active", button.dataset.radarScope === activeRadarScope);
  });

  if (!candidates.length) {
    const loading = loadState === "loading" && !sectors.length;
    outlierRows.innerHTML = `
      <div class="outlier-empty" role="row">
        <strong>${loading ? "Scanning outliers" : "No outliers yet"}</strong>
        <span>${loading ? "Live Binance data is loading. Core scan usually takes 20-30 seconds." : selectedSector ? `No ${selectedSector.name} pairs pass the radar filter yet.` : "Waiting for relative strength, OI, CVD or volume confirmation."}</span>
      </div>
    `;
    renderOutlookCockpit([]);
    return;
  }

  if (!selectedOutlierSymbol || !candidates.some((candidate) => candidate.symbol === selectedOutlierSymbol)) {
    selectedOutlierSymbol = candidates[0].symbol;
  }

  outlierRows.innerHTML = candidates
    .map(
      (candidate) => `
        <button class="outlier-row${candidate.symbol === selectedOutlierSymbol ? " is-selected" : ""}" type="button" data-symbol="${candidate.symbol}" role="row">
          <span class="outlier-asset" role="cell">
            <strong>${candidate.symbol}</strong>
            <small>${candidate.sector}</small>
          </span>
          <span role="cell"><b class="stage-badge ${candidate.className}">${candidate.label}</b></span>
          <span role="cell"><b class="score-pill">${candidate.score}</b></span>
          <span role="cell"><b class="volume-ratio">${formatVolumeRatio(candidate.volumeTo24h)}</b></span>
          <span role="cell"><b class="volume-ratio">${formatPct(candidate.baseDistance)}</b></span>
          <span role="cell"><b class="volume-ratio">${formatPct(candidate.oiToMcap).replace("+", "")}</b></span>
          <span role="cell"><b class="volume-ratio">${formatDailyFvg(candidate)}</b></span>
          <span role="cell"><b class="volume-ratio">${activeHorizon === "intrawick" ? `${candidate.emaTrend}/4` : formatPct(candidate.boxRange).replace("+", "")}</b></span>
          <span class="${signedClass(candidate.breakoutPct)}" role="cell">${formatPct(candidate.breakoutPct)}</span>
          <span class="${signedClass(candidate.rs1h)}" role="cell">${formatPct(candidate.rs1h)}</span>
          <span class="${signedClass(candidate.rs24h)}" role="cell">${formatPct(candidate.rs24h)}</span>
          <span class="${signedClass(candidate.oiChange)}" role="cell">${formatPct(candidate.oiChange)}</span>
          <span class="${signedClass(candidate.flowUsd)}" role="cell">${activeHorizon === "intrawick" ? formatPct(candidate.flowIntensity) : formatMoney(candidate.flowUsd)}</span>
          <span class="outlier-read" role="cell">${candidate.read}</span>
        </button>
      `
    )
    .join("");

  renderOutlookCockpit(candidates);
}

function getConfluenceChecks(candidate) {
  return [
    {
      label: "Multi-day base",
      passed: candidate.baseDays >= 10 && candidate.baseRange > 0,
      value: candidate.baseDays ? `${candidate.baseDays}D / ${candidate.baseRange.toFixed(1)}%` : "waiting"
    },
    {
      label: "Near base high",
      passed: candidate.baseDistance >= -5,
      value: `${formatPct(candidate.baseDistance)} vs base high`
    },
    {
      label: "Dry-up then expansion",
      passed: candidate.baseDryUp > 0 && candidate.baseDryUp <= 1.05 && candidate.basePrebreakVolume >= 0.9,
      value: `${candidate.baseDryUp.toFixed(2)}x dry / ${candidate.basePrebreakVolume.toFixed(2)}x live`
    },
    {
      label: "1H consolidation box",
      passed: candidate.boxRange > 0 && candidate.boxRange <= 3.2,
      value: candidate.boxRange > 0 ? `${candidate.boxRange.toFixed(2)}% range` : "waiting"
    },
    {
      label: "Box high breakout",
      passed: candidate.breakoutPct >= 0.18,
      value: `${formatPct(candidate.breakoutPct)} vs box high`
    },
    {
      label: "Relative strength vs sector",
      passed: candidate.rs1h > 0.8 || candidate.rs24h > 4,
      value: `${formatPct(candidate.rs1h)} 1H / ${formatPct(candidate.rs24h)} 24H`
    },
    {
      label: "Daily FVG test",
      passed: candidate.dailyFvgTest === true,
      value: candidate.dailyFvgSide
        ? `${formatDailyFvg(candidate)} / ${candidate.dailyFvgAgeDays ?? "-"}D old`
        : "none nearby"
    },
    {
      label: "4H/1D EMA support",
      passed: candidate.emaTrend >= 2,
      value: `${candidate.emaTrend}/4 zones above`
    },
    {
      label: "Market outperformance",
      passed: candidate.marketRs > 5,
      value: `${formatPct(candidate.marketRs)} vs market 24H`
    },
    {
      label: "OI expansion",
      passed: candidate.oiChange > 3,
      value: formatPct(candidate.oiChange)
    },
    {
      label: "OI / market cap",
      passed: candidate.oiToMcap >= 0.8,
      value: `${formatPct(candidate.oiToMcap).replace("+", "")} OI/MCAP`
    },
    {
      label: "Positive TCD/CVD",
      passed: candidate.flowUsd > 0,
      value: formatMoney(candidate.flowUsd)
    },
    {
      label: "TCD/CVD intensity",
      passed: candidate.flowIntensity > 0.08,
      value: `${formatPct(candidate.flowIntensity)} vs 24H volume`
    },
    {
      label: "Orderbook pressure",
      passed: Math.abs(numberOr(candidate.obImbalance)) >= 12,
      value: formatOrderBookPressure(candidate.obImbalance)
    },
    {
      label: "Volume expansion",
      passed: candidate.volumeTo24h >= 0.55 || candidate.volumeSpike > 1.5 || candidate.volumeSpike15m > 1.5,
      value: `${formatVolumeRatio(candidate.volumeTo24h)} of 24H / ${candidate.volumeSpike15m.toFixed(2)}x 15M`
    },
    {
      label: "Liquidation not overheated",
      passed: candidate.liqPct < 8,
      value: `${numberOr(candidate.liqPct).toFixed(2)}% LIQ`
    }
  ];
}

function getOutlookLevels(candidate) {
  const price = candidate.price || 1;
  const heat = Math.min(Math.max(Math.abs(candidate.rs24h) / 100, 0.02), 0.18);
  const breakout = Number.isFinite(candidate.breakoutLevel) && candidate.breakoutLevel > 0
    ? candidate.breakoutLevel
    : price * (1 + Math.max(0.018, heat * 0.45));
  return [
    ["Now", price],
    ["Base High", candidate.baseHigh],
    ["Box High", breakout],
    ["Support", price * (1 - Math.max(0.018, heat * 0.35))],
    ["Must-hold", price * (1 - Math.max(0.035, heat * 0.65))]
  ];
}

function formatDailyFvg(candidate) {
  if (!candidate.dailyFvgSide) return "-";
  const side = candidate.dailyFvgSide === "bullish" ? "Bull" : "Bear";
  if (candidate.dailyFvgTest) return `${side} test`;
  if (!Number.isFinite(candidate.dailyFvgDistance)) return side;
  return `${side} ${formatPct(candidate.dailyFvgDistance)}`;
}

function getEmaZones(candidate) {
  return [
    ["4H EMA50", candidate.ema4h50],
    ["4H EMA100", candidate.ema4h100],
    ["1D EMA50", candidate.ema1d50],
    ["1D EMA100", candidate.ema1d100]
  ].map(([label, value]) => {
    const numeric = Number.isFinite(value) ? value : null;
    const distance = numeric && candidate.price ? ((candidate.price / numeric) - 1) * 100 : null;
    return { label, value: numeric, distance };
  });
}

function formatEmaDistance(distance) {
  if (!Number.isFinite(distance)) return "waiting";
  if (distance >= 0) return `${formatPct(distance)} above`;
  return `${formatPct(distance)} below`;
}

function renderOutlookCockpit(candidates) {
  if (!outlookAsset) return;
  const candidate = candidates.find((item) => item.symbol === selectedOutlierSymbol) || candidates[0];

  if (!candidate) {
    outlookAsset.textContent = "-";
    outlookSubtitle.textContent = loadState === "loading" ? "Scanning live data" : "No active outlier candidate";
    outlookConfluence.textContent = "0/6";
    outlookScore.textContent = "score 0";
    outlookStage.textContent = "Watchlist";
    outlookStage.className = "stage-badge stage-watch";
    outlookRead.textContent = loadState === "loading" ? "Loading market snapshots, OI, CVD and orderbook metrics." : "Waiting for stronger confirmation.";
    outlookLevels.innerHTML = "";
    outlookEmaZones.innerHTML = "";
    outlookConfluenceList.innerHTML = "";
    outlookBullish.innerHTML = "";
    outlookBearish.innerHTML = "";
    return;
  }

  const checks = getConfluenceChecks(candidate);
  const passedCount = checks.filter((item) => item.passed).length;
  const levels = getOutlookLevels(candidate);
  const emaZones = getEmaZones(candidate);

  outlookAsset.textContent = candidate.symbol;
  outlookSubtitle.textContent = `${candidate.sector} / ${formatLevel(candidate.displayPrice ?? candidate.price)} / ${activeHorizon} / ${candidate.label}`;
  outlookConfluence.textContent = `${passedCount}/${checks.length}`;
  outlookScore.textContent = `score ${candidate.score}`;
  outlookStage.textContent = candidate.label;
  outlookStage.className = `stage-badge ${candidate.className}`;
  outlookRead.textContent = candidate.read;

  outlookLevels.innerHTML = levels
    .map(
      ([label, value]) => `
        <div class="level-tile">
          <span>${label}</span>
          <strong>${formatLevel(value)}</strong>
        </div>
      `
    )
    .join("");

  outlookEmaZones.innerHTML = emaZones
    .map(
      (zone) => `
        <div class="ema-tile ${Number.isFinite(zone.distance) && zone.distance >= 0 ? "is-support" : ""}">
          <span>${zone.label}</span>
          <strong>${formatLevel(zone.value)}</strong>
          <small>${formatEmaDistance(zone.distance)}</small>
        </div>
      `
    )
    .join("");

  outlookConfluenceList.innerHTML = checks
    .map(
      (item) => `
        <div class="check-item ${item.passed ? "is-confirmed" : ""}">
          <i>${item.passed ? "OK" : "WAIT"}</i>
          <span>${item.label}</span>
          <strong>${item.value}</strong>
        </div>
      `
    )
    .join("");

  outlookBullish.innerHTML = [
    `Hold above support near ${formatLevel(levels[2][1])}.`,
    `Reclaim breakout near ${formatLevel(levels[1][1])} with volume/OI confirmation.`,
    "Keep TCD/CVD positive and stronger than normal relative to 24H volume.",
    "Prefer bid-side orderbook pressure while price holds above support.",
    "Respect 4H/1D EMA zones as support on pullbacks."
  ]
    .map((item) => `<li>${item}</li>`)
    .join("");

  outlookBearish.innerHTML = [
    `Lose must-hold near ${formatLevel(levels[3][1])}.`,
    "Lose EMA50/EMA100 support on 4H or daily close.",
    "OI rises while TCD/CVD turns negative.",
    "Ask walls dominate while price fails to reclaim the breakout level.",
    candidate.liqPct >= 8 ? "Liquidation pressure is already hot." : "LIQ pressure spikes above the current zone."
  ]
    .map((item) => `<li>${item}</li>`)
    .join("");
}

function renderDocs() {
  docsGrid.innerHTML = metricDocs
    .map(
      (doc) => `
        <article class="doc-card">
          <h3>${doc.title}</h3>
          <p>${doc.read}</p>
          <code>${doc.formula}</code>
          <span class="doc-source">${doc.source}</span>
        </article>
      `
    )
    .join("");
}

function renderRows() {
  const rows = getFilteredSectors();

  if (!sectors.length && loadState === "loading") {
    sectorRows.innerHTML = `
      <div class="empty-state" role="row">
        <strong>Scanning live market data</strong>
        <span>Fetching price, OI, CVD, volume, EMA zones and orderbook pressure.</span>
      </div>
    `;
    renderDetail(null);
    return;
  }

  if (!rows.some((sector) => sector.name === selectedName) && rows.length) {
    selectedName = rows[0].name;
  }

  if (!rows.length) {
    const isUnavailable = !sectors.length && loadState === "error";
    sectorRows.innerHTML = `
      <div class="empty-state" role="row">
        <strong>${isUnavailable ? "Market data unavailable" : "No sectors found"}</strong>
        <span>${isUnavailable ? "Live API did not return usable data. Refresh to try again." : "Try another search or filter."}</span>
      </div>
    `;
    renderDetail(null);
    return;
  }

  sectorRows.innerHTML = rows
    .map((sector) => {
      const selected = sector.name === selectedName ? " is-selected" : "";
      const signal = getSignal(sector);
      const cvd = numberOr(sector.cvd);
      const cvdMeter = Math.min(Math.abs(cvd) / 80000000, 1);
      const longPct = Math.max(0, Math.min(numberOr(sector.longPct, 50), 100));
      const shortPct = Math.max(0, Math.min(numberOr(sector.shortPct, 50), 100));
      const exchanges = getSectorExchanges(sector);

      return `
        <button class="screener-row${selected}" type="button" data-sector="${sector.name}" role="row">
          <span class="sector-cell" role="cell">
            <strong>${sector.name}</strong>
            <small>${sector.tokens.length} members <em class="${signedClass(sector.perf24h)}">24H ${formatPct(sector.perf24h)}</em></small>
          </span>
          <span role="cell">${numberOr(sector.index).toFixed(2)}</span>
          <span role="cell"><b class="direction-badge ${signal.className}">${signal.symbol} ${signal.label}</b></span>
          <span class="long-short-cell" role="cell">
            <b>${longPct}%</b>
            <i class="ls-row-bar" aria-hidden="true"><em style="width:${longPct}%"></em><strong style="width:${shortPct}%"></strong></i>
            <b>${shortPct}%</b>
          </span>
          <span class="${signedClass(sector.oiChange)}" role="cell">${formatPct(sector.oiChange)}</span>
          <span role="cell">${formatMoney(sector.oiUsd)}</span>
          <span class="cvd-cell ${signedClass(cvd)}" role="cell">
            <i class="cvd-mini-bar ${cvd < 0 ? "is-negative" : ""}" aria-hidden="true"><em style="--meter:${cvdMeter}"></em></i>
            <b>${formatMoney(cvd)}</b>
          </span>
          <span class="exchange-cell" role="cell">
            ${exchanges.map((exchange) => `<b>${exchange}</b>`).join("")}
          </span>
        </button>
      `;
    })
    .join("");

  const selected = sectors.find((sector) => sector.name === selectedName) || rows[0] || sectors[0];
  renderDetail(selected);
}

function renderDetail(sector) {
  if (!sector) {
    const isLoading = loadState === "loading";
    const isUnavailable = loadState === "error";
    document.querySelector("#detailTag").textContent = isLoading ? "Live scan" : isUnavailable ? "Unavailable" : "No selection";
    document.querySelector("#detailName").textContent = isLoading ? "Scanning" : "-";
    document.querySelector("#detailDescription").textContent = isLoading
      ? "Waiting for Binance snapshots."
      : isUnavailable
      ? "No usable live market payload is available right now."
      : "Select a sector from the table.";
    document.querySelector("#setupLabel").textContent = isLoading ? "Loading" : isUnavailable ? "Unavailable" : "Watchlist";
    document.querySelector("#setupLabel").className = "setup-badge setup-neutral";
    document.querySelector("#setupReason").textContent = isLoading
      ? "The first live scan can take about 20-30 seconds."
      : isUnavailable
      ? "Refresh when the API is available again."
      : "No sector selected.";
    document.querySelector("#setupConfidence").textContent = isLoading ? "loading" : isUnavailable ? "offline" : "idle";
    document.querySelector("#detailIndex").textContent = "-";
    document.querySelector("#liqPressure").textContent = "-";
    document.querySelector("#liqMeter").style.width = "0%";
    document.querySelector("#longShort").textContent = "-";
    document.querySelector("#longBar").style.width = "50%";
    document.querySelector("#shortBar").style.width = "50%";
    document.querySelector("#oiValue").textContent = "-";
    document.querySelector("#oiChange").textContent = "-";
    document.querySelector("#cvdValue").textContent = "-";
    document.querySelector("#cvdSide").textContent = "-";
    document.querySelector("#obValue").textContent = "-";
    document.querySelector("#obSide").textContent = "-";
    document.querySelector("#memberCount").textContent = "0 members";
    memberChips.innerHTML = "";
    tokenRows.innerHTML = "";
    return;
  }

  const setup = getSetup(sector);

  document.querySelector("#detailTag").textContent = "Equal weighted";
  document.querySelector("#detailName").textContent = sector.name;
  document.querySelector("#detailDescription").textContent = sector.description;
  document.querySelector("#setupLabel").textContent = setup.label;
  document.querySelector("#setupLabel").className = `setup-badge ${setup.className}`;
  document.querySelector("#setupReason").textContent = setup.reason;
  document.querySelector("#setupConfidence").textContent = setup.confidence;
  document.querySelector("#detailIndex").textContent = numberOr(sector.index).toFixed(2);
  document.querySelector("#liqPressure").textContent = `${numberOr(sector.liqPct).toFixed(2)}%`;
  document.querySelector("#liqMeter").style.width = `${Math.min(numberOr(sector.liqPct), 14) / 14 * 100}%`;
  document.querySelector("#longShort").textContent = `${numberOr(sector.longPct, 50)} / ${numberOr(sector.shortPct, 50)}`;
  document.querySelector("#longBar").style.width = `${numberOr(sector.longPct, 50)}%`;
  document.querySelector("#shortBar").style.width = `${numberOr(sector.shortPct, 50)}%`;
  document.querySelector("#oiValue").textContent = formatMoney(sector.oiUsd);
  document.querySelector("#oiChange").textContent = formatPct(sector.oiChange);
  document.querySelector("#oiChange").className = signedClass(sector.oiChange);
  document.querySelector("#cvdValue").textContent = formatMoney(sector.cvd);
  document.querySelector("#cvdValue").className = signedClass(sector.cvd);
  document.querySelector("#cvdSide").textContent = sector.cvd >= 0 ? "buyers" : "sellers";
  document.querySelector("#obValue").textContent = formatOrderBookPressure(sector.obImbalance);
  document.querySelector("#obValue").className = signedClass(sector.obImbalance);
  document.querySelector("#obSide").textContent = `bid ${formatMoney(sector.obBidWallUsd)} / ask ${formatMoney(sector.obAskWallUsd)}`;
  document.querySelector("#memberCount").textContent = `${sector.tokens.length} members`;

  memberChips.innerHTML = sector.tokens
    .map((token) => `<span class="member-chip">${token.symbol}</span>`)
    .join("");

  tokenRows.innerHTML = sector.tokens
    .map(
      (token) => {
        const volume5m = estimateVolume5m(token, sector);
        const volumeRatio = volumeTo24hPct(volume5m, numberOr(token.volume));
        const pairFlow = getPairLongShort(token, sector);
        const pairSignal = getPairSignal(token, sector);

        return `
          <div class="token-row" role="row">
            <span role="cell">${token.symbol}</span>
            <span role="cell"><b class="pair-signal ${pairSignal.className}" title="${pairFlow.source === "pair" ? "Pair liquidation split" : "Derived from pair flow + sector split"}">${pairSignal.symbol} ${pairSignal.label}</b></span>
            <span role="cell">${formatPrice(token.displayPrice ?? token.price)}</span>
            <span class="pair-ls-cell" role="cell">
              <b>${pairFlow.longPct}%</b>
              <i class="pair-ls-bar" aria-hidden="true"><em style="width:${pairFlow.longPct}%"></em><strong style="width:${pairFlow.shortPct}%"></strong></i>
              <b>${pairFlow.shortPct}%</b>
            </span>
            <span class="${signedClass(token.perf24h)}" role="cell">${formatPct(token.perf24h)}</span>
            <span role="cell"><b class="volume-ratio">${formatVolumeRatio(volumeRatio)}</b></span>
            <span role="cell">${formatMoney(token.volume)}</span>
          </div>
        `;
      }
    )
    .join("");
}

sectorRows.addEventListener("click", (event) => {
  const row = event.target.closest(".screener-row");
  if (!row) return;
  selectedName = row.dataset.sector;
  if (activeRadarScope === "sector") {
    selectedOutlierSymbol = null;
  }
  renderRows();
  renderOutlierRadar();
});

outlierRows?.addEventListener("click", (event) => {
  const row = event.target.closest(".outlier-row");
  if (!row) return;
  selectedOutlierSymbol = row.dataset.symbol;
  renderOutlierRadar();
});

searchInput.addEventListener("input", renderRows);
sortSelect.addEventListener("change", renderRows);
scanModeSelect?.addEventListener("change", () => {
  activeScanMode = scanModeSelect.value;
  selectedOutlierSymbol = null;
  hydrateFromApi();
});

refreshButton?.addEventListener("click", () => {
  hydrateFromApi();
});

horizonSelect?.addEventListener("change", () => {
  activeHorizon = horizonSelect.value;
  selectedOutlierSymbol = null;
  renderSignals();
  renderRows();
  renderOutlierRadar();
});

radarScopeButtons.forEach((button) => {
  button.addEventListener("click", () => {
    activeRadarScope = button.dataset.radarScope || "market";
    selectedOutlierSymbol = null;
    renderOutlierRadar();
  });
});

filterButtons.forEach((button) => {
  button.addEventListener("click", () => {
    activeFilter = button.dataset.filter;
    filterButtons.forEach((item) => item.classList.toggle("is-active", item === button));
    renderRows();
  });
});

renderDocs();
renderSignals();
renderRows();
renderOutlierRadar();
hydrateFromApi();

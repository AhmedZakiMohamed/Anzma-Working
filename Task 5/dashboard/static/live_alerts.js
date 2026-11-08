(function () {
  var ALERT_CHECK_INTERVAL_MS = 10000;
  var SCENARIOS = ["baseline", "S1", "S2", "S3", "S4", "S5"];

  function createBanner() {
    var existing = document.getElementById("criticalAlertBanner");

    if (existing) {
      return existing;
    }

    var banner = document.createElement("div");
    banner.id = "criticalAlertBanner";
    banner.setAttribute("role", "alert");
    banner.style.position = "fixed";
    banner.style.top = "80px";
    banner.style.left = "24px";
    banner.style.right = "24px";
    banner.style.zIndex = "99999";
    banner.style.padding = "18px 24px";
    banner.style.background = "#dc2626";
    banner.style.color = "#ffffff";
    banner.style.fontWeight = "800";
    banner.style.fontSize = "17px";
    banner.style.lineHeight = "1.5";
    banner.style.borderRadius = "12px";
    banner.style.border = "3px solid #ffffff";
    banner.style.boxShadow = "0 10px 30px rgba(0, 0, 0, 0.45)";
    banner.style.display = "none";
    banner.style.cursor = "pointer";
    banner.style.textAlign = "center";

    banner.addEventListener("click", function () {
      var alertsSection =
        document.getElementById("alerts") ||
        document.getElementById("alerts-section") ||
        document.getElementById("alertsPanel") ||
        document.querySelector("[data-section='alerts']");

      if (alertsSection) {
        alertsSection.scrollIntoView({ behavior: "smooth" });
      }
    });

    document.body.appendChild(banner);
    return banner;
  }

  function buildMessage(criticalIncidents) {
    var first = criticalIncidents[0];
    var asset = first.asset_code || "Unknown asset";
    var metric = first.metric || "Unknown metric";
    var scenario = first.scenario || "unknown scenario";

    return (
      "🚨 LIVE CRITICAL ALERT: " +
      criticalIncidents.length +
      " critical incident" +
      (criticalIncidents.length === 1 ? "" : "s") +
      " detected. " +
      "Scenario: " +
      scenario +
      ". Affected asset: " +
      asset +
      " — " +
      metric +
      ". Click here to view alerts."
    );
  }

  function showCriticalAlert(banner, criticalIncidents) {
    if (criticalIncidents.length === 0) {
      banner.style.display = "none";
      banner.textContent = "";
      return;
    }

    banner.textContent = buildMessage(criticalIncidents);
    banner.style.display = "block";
  }

  async function checkScenario(scenario) {
    var response = await fetch(
      "/api/v1/dashboard/alerts?scenario=" + encodeURIComponent(scenario),
      {
        headers: {
          Accept: "application/json",
        },
      }
    );

    if (!response.ok) {
      return [];
    }

    var data = await response.json();
    var incidents = data.incidents || [];

    return incidents
      .filter(function (incident) {
        return incident && incident.severity === "critical";
      })
      .map(function (incident) {
        return Object.assign({}, incident, { scenario: scenario });
      });
  }

  async function checkAllCriticalAlerts() {
    var banner = createBanner();
    var allCriticalIncidents = [];

    try {
      var results = await Promise.all(
        SCENARIOS.map(function (scenario) {
          return checkScenario(scenario);
        })
      );

      results.forEach(function (incidents) {
        allCriticalIncidents = allCriticalIncidents.concat(incidents);
      });

      showCriticalAlert(banner, allCriticalIncidents);
    } catch (error) {
      banner.style.display = "none";
      banner.textContent = "";
    }
  }

  function startLiveAlerts() {
    checkAllCriticalAlerts();
    setInterval(checkAllCriticalAlerts, ALERT_CHECK_INTERVAL_MS);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", startLiveAlerts);
  } else {
    startLiveAlerts();
  }
})();
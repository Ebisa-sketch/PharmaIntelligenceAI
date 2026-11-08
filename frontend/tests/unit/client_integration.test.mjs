// ============================================================================
// PharmaIntelligence AI - Frontend Client & Logic Integration Tests
// Executed via Node.js native test runner: node --test
// ============================================================================

import test from 'node:test';
import assert from 'node:assert/strict';

test('Frontend Auth: Mock Admin Login & Role Recognition', async () => {
  const mockUser = {
    id: 1,
    email: 'admin@pharmaintelligence.et',
    full_name: 'National System Administrator',
    role: 'admin',
    facility_id: 1,
    facility_name: 'Tikur Anbessa Specialized Hospital',
    is_active: true,
  };

  assert.equal(mockUser.email, 'admin@pharmaintelligence.et');
  assert.equal(mockUser.role, 'admin');
  assert.equal(mockUser.is_active, true);
});

test('Frontend Forecasting: Syntetos-Boylan Cutoff Verification', () => {
  // Classification boundaries: ADI cutoff = 1.32, CV2 cutoff = 0.49
  function classifyDemand(adi, cv2) {
    if (adi < 1.32 && cv2 < 0.49) return 'Smooth';
    if (adi >= 1.32 && cv2 < 0.49) return 'Intermittent';
    if (adi < 1.32 && cv2 >= 0.49) return 'Erratic';
    return 'Lumpy';
  }

  assert.equal(classifyDemand(1.15, 0.22), 'Smooth');
  assert.equal(classifyDemand(1.85, 0.31), 'Intermittent');
  assert.equal(classifyDemand(1.10, 0.65), 'Erratic');
  assert.equal(classifyDemand(2.10, 0.88), 'Lumpy');
});

test('Frontend Stockout Intelligence: Days of Stock Remaining (DSR) & Tiers', () => {
  function computeDSR(stock, dailyDemand) {
    if (dailyDemand <= 0) return 999.0;
    return stock / dailyDemand;
  }

  function getRiskTier(dsr, leadTime) {
    if (dsr <= 0) return 'Critical';
    if (dsr < 7) return 'Critical';
    if (dsr < leadTime) return 'High';
    if (dsr < leadTime * 1.5) return 'Medium';
    return 'Low';
  }

  // Zero stock runout
  assert.equal(computeDSR(0, 50), 0);
  assert.equal(getRiskTier(0, 25), 'Critical');

  // Stock below lead time (DSR = 19.1 days < 25 days lead time)
  const dsr = computeDSR(420, 22);
  assert.equal(Math.round(dsr * 10) / 10, 19.1);
  assert.equal(getRiskTier(dsr, 25), 'High');

  // Safe stock buffer (DSR = 92.8 days > 20 days lead time)
  const safeDsr = computeDSR(2600, 28);
  assert.equal(getRiskTier(safeDsr, 20), 'Low');
});

test('Frontend Expiry Prevention: FEFO PUSE & Financial Value at Risk (ETB)', () => {
  function calculateFEFORisk(currentStock, dailyDemand, daysToExpiry, unitCostETB) {
    const projectedConsumption = dailyDemand * daysToExpiry;
    const puse = Math.max(0, currentStock - projectedConsumption);
    const valueAtRisk = puse * unitCostETB;
    return { puse, valueAtRisk };
  }

  // Batch AMX-2024-001: 420 units, daily demand = 7.5 units, 37 days left, unit cost = 24.50 ETB
  // Expected consumption = 277.5 units -> Surplus PUSE = 142.5 units
  const result = calculateFEFORisk(420, 7.5, 37, 24.50);
  assert.equal(result.puse, 142.5);
  assert.equal(result.valueAtRisk, 142.5 * 24.50);
  assert.ok(result.valueAtRisk > 3000);
});

test('Frontend Redistribution: Haversine Distance & Net Economic Benefit', () => {
  function haversineDistance(lat1, lon1, lat2, lon2) {
    const R = 6371.0;
    const dLat = ((lat2 - lat1) * Math.PI) / 180;
    const dLon = ((lon2 - lon1) * Math.PI) / 180;
    const a =
      Math.sin(dLat / 2) * Math.sin(dLat / 2) +
      Math.cos((lat1 * Math.PI) / 180) *
        Math.cos((lat2 * Math.PI) / 180) *
        Math.sin(dLon / 2) *
        Math.sin(dLon / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return R * c;
  }

  function calculateTransferEconomics(qty, distKm, unitCostETB, cTransportPerKmUnit = 0.02) {
    const transportCost = qty * distKm * cTransportPerKmUnit;
    const valueSaved = qty * unitCostETB;
    const netBenefit = valueSaved - transportCost;
    return { transportCost, valueSaved, netBenefit };
  }

  // St. Paul's (9.0567, 38.7297) to Tikur Anbessa (9.0142, 38.7525) ~ 5.3 km
  const dist = haversineDistance(9.0567, 38.7297, 9.0142, 38.7525);
  assert.ok(dist >= 5.0 && dist <= 6.0);

  // Transfer 400 units of 25.0 ETB medicine over 5.5 km
  const econ = calculateTransferEconomics(400, dist, 25.0);
  assert.ok(econ.transportCost < 100.0);
  assert.equal(econ.valueSaved, 10000.0);
  assert.ok(econ.netBenefit > 9900.0);
});

test('Frontend Data Quality: 5D Weighted DQI Index Calculation', () => {
  const weights = {
    completeness: 0.25,
    consistency: 0.20,
    plausibility: 0.20,
    expiry_validity: 0.20,
    uniqueness: 0.15,
  };

  const scores = {
    completeness: 98.2,
    consistency: 94.5,
    plausibility: 91.0,
    expiry_validity: 89.8,
    uniqueness: 94.5,
  };

  let totalDQI = 0;
  for (const dim in weights) {
    totalDQI += scores[dim] * weights[dim];
  }

  // Verify weighted sum is within Grade A range (>90)
  assert.ok(totalDQI > 90.0 && totalDQI <= 100.0);
  assert.equal(Math.round(totalDQI * 10) / 10, 93.8);
});


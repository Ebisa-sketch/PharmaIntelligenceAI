// ============================================================================
// PharmaIntelligence AI - TypeScript Type Definitions
// ============================================================================

export type RoleName = 'admin' | 'pharmacy_manager' | 'regional_manager' | 'data_analyst' | 'auditor';

export interface User {
  id: number;
  email: string;
  full_name: string;
  role: RoleName | string;
  facility_id?: number | null;
  facility_name?: string | null;
  is_active: boolean;
  created_at?: string;
}

export interface AuthToken {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
}

export interface LoginResponse {
  token: AuthToken;
  user: User;
}

export interface Facility {
  id: number;
  code: string;
  name: string;
  facility_type: string;
  region: string;
  zone?: string | null;
  woreda?: string | null;
  latitude: number;
  longitude: number;
  storage_capacity_m3: number;
  is_active: boolean;
  created_at?: string;
}

export interface Medicine {
  id: number;
  code: string;
  name: string;
  brand_name?: string | null;
  category: string;
  dosage_form: string;
  strength: string;
  unit_of_measure: string;
  is_essential: boolean;
  vital_classification: 'Vital' | 'Essential' | 'Non-essential' | string;
  minimum_stock_level: number;
  reorder_point: number;
  lead_time_days: number;
  created_at?: string;
}

export interface InventoryItem {
  id: number;
  facility_id: number;
  facility_name?: string;
  medicine_id: number;
  medicine_name?: string;
  medicine_code?: string;
  current_quantity: number;
  allocated_quantity: number;
  available_quantity: number;
  reorder_level: number;
  lead_time_days: number;
  stock_status: 'Adequate' | 'Understocked' | 'Overstocked' | 'Stockout' | string;
  last_counted_at?: string | null;
  updated_at?: string;
}

export interface BatchItem {
  id: number;
  batch_number: string;
  medicine_id: number;
  medicine_name?: string;
  medicine_code?: string;
  facility_id: number;
  facility_name?: string;
  manufacturing_date?: string | null;
  expiry_date: string;
  initial_quantity: number;
  current_quantity: number;
  unit_cost: number;
  status: 'Active' | 'Quarantined' | 'Expired' | 'Depleted' | string;
  days_to_expiry?: number;
  created_at?: string;
}

export interface InventoryTransaction {
  id: number;
  facility_id: number;
  facility_name?: string;
  medicine_id: number;
  medicine_name?: string;
  batch_id?: number | null;
  batch_number?: string | null;
  transaction_type: 'Receipt' | 'Issue' | 'Transfer In' | 'Transfer Out' | 'Adjustment' | 'Disposal';
  quantity: number;
  balance_after: number;
  reference_number?: string | null;
  notes?: string | null;
  created_at: string;
  created_by?: number | null;
}

export interface DataQualityDimension {
  score: number;
  status: 'OPTIMAL' | 'ACCEPTABLE' | 'DEGRADED' | 'CRITICAL';
  details: string;
}

export interface DataQualityScorecard {
  facility_id: number;
  facility_name?: string;
  overall_dqi: number;
  quality_grade: string;
  assessed_at: string;
  dimensions: {
    completeness: DataQualityDimension;
    consistency: DataQualityDimension;
    plausibility: DataQualityDimension;
    expiry_validity: DataQualityDimension;
    uniqueness: DataQualityDimension;
  };
  total_issues_found: number;
  critical_issues_count: number;
}

export interface DataQualityIssue {
  id: number;
  import_id?: number | null;
  facility_id: number;
  facility_name?: string | null;
  medicine_id?: number | null;
  medicine_name?: string | null;
  issue_type: string;
  severity: 'CRITICAL' | 'WARNING' | 'INFO';
  field_name?: string | null;
  row_number?: number | null;
  description: string;
  details?: Record<string, any> | null;
  is_resolved: boolean;
  created_at: string;
}

export interface ForecastPoint {
  date: string;
  historical_consumption?: number | null;
  predicted_demand: number;
  p10: number;
  p50: number;
  p90: number;
}

export interface ForecastResponse {
  facility_id: number;
  medicine_id: number;
  medicine_name?: string;
  horizon_days: number;
  model_type: string;
  generated_at: string;
  points: ForecastPoint[];
  summary: {
    total_projected_demand: number;
    daily_average_demand: number;
    recommended_safety_stock: number;
    demand_pattern: string;
    volatility: string;
  };
}

export interface ModelMetric {
  model_name: string;
  rmse: number;
  mae: number;
  wape: number;
  mape: number;
  mase: number;
  rank: number;
  recommended: boolean;
}

export interface ModelComparisonResponse {
  facility_id: number;
  medicine_id: number;
  medicine_name: string;
  syntetos_boylan_class: 'Smooth' | 'Intermittent' | 'Erratic' | 'Lumpy';
  adi: number;
  cv2: number;
  classification_rationale: string;
  models: ModelMetric[];
  best_model: string;
}

export interface StockoutRiskItem {
  id?: number;
  facility_id: number;
  facility_name?: string;
  medicine_id: number;
  medicine_name: string;
  medicine_code: string;
  vital_classification: string;
  current_stock: number;
  daily_demand_rate: number;
  days_of_stock_remaining: number;
  lead_time_days: number;
  stockout_probability: number;
  risk_level: 'Critical' | 'High' | 'Medium' | 'Low';
  risk_horizon_days: number;
  confidence_score: number;
  feature_attributions: {
    feature: string;
    impact: number;
    direction: 'increases_risk' | 'decreases_risk';
  }[];
  clinical_recommendation: string;
}

export interface ExpiryRiskItem {
  id?: number;
  facility_id: number;
  facility_name?: string;
  batch_id: number;
  batch_number: string;
  medicine_id: number;
  medicine_name: string;
  current_quantity: number;
  unit_cost: number;
  expiry_date: string;
  days_until_expiry: number;
  projected_unused_stock: number;
  financial_value_at_risk_etb: number;
  risk_level: 'Critical' | 'High' | 'Medium' | 'Low';
  action_recommendation: string;
}

export interface RedistributionProposal {
  id: number;
  source_facility_id: number;
  source_facility_name: string;
  target_facility_id: number;
  target_facility_name: string;
  medicine_id: number;
  medicine_name: string;
  medicine_code: string;
  batch_id: number;
  batch_number: string;
  recommended_quantity: number;
  distance_km: number;
  transport_cost_etb: number;
  net_value_saved_etb: number;
  priority: 'High' | 'Medium' | 'Low';
  status: 'Pending' | 'Approved' | 'Rejected' | 'In Transit' | 'Completed';
  created_at: string;
  shelf_life_viable: boolean;
  donor_safety_stock_protected: boolean;
  recipient_deficit_resolved: boolean;
  rejection_reason?: string | null;
}

export interface SystemSummary {
  total_facilities: number;
  total_inventory_items: number;
  critical_stockouts: number;
  active_monitored_batches: number;
  pending_redistribution_recommendations: number;
  average_dqi_score: number;
}

export interface AuditLogEntry {
  id: number;
  user_id?: number | null;
  user_email?: string | null;
  action: string;
  entity_type: string;
  entity_id?: string | number | null;
  details?: Record<string, any> | string | null;
  ip_address?: string | null;
  timestamp: string;
}

export interface ExperimentRun {
  experiment_id: string;
  name: string;
  status: 'Completed' | 'Running' | 'Queued' | 'Failed';
  evaluation_metrics: {
    baseline_mape?: number;
    ai_ensemble_mape?: number;
    stockout_reduction_pct?: number;
    expiry_reduction_pct?: number;
    feature_stability_score?: number;
    mean_explanation_latency_ms?: number;
    wape?: number;
    mase?: number;
  };
  timestamp: string;
}

export interface FacilityReport {
  facility_id: number;
  facility_name: string;
  region: string;
  total_tracked_medicines: number;
  stockout_count: number;
  understocked_count: number;
  total_active_batches: number;
}

export interface SystemSettings {
  auto_reorder_enabled: boolean;
  donor_safety_stock_buffer_days: number;
  max_transfer_radius_km: number;
  stockout_alert_threshold_dsr: number;
  expiry_warning_threshold_days: number;
  fefo_strict_mode: boolean;
  sms_alert_notifications: boolean;
  email_digest_frequency: 'Daily' | 'Weekly' | 'Realtime';
}



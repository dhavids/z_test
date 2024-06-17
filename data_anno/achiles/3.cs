
public class MicrosoftAPIEndpoints
{
    public const string BaseUrl = "https://api.partnercenter.microsoft.com";
    public const string AzureADLoginEndpoint = "https://login.microsoftonline.com/{CSPTenantID}/oauth2/token";

    public class Endpoints
    {
        public const string AgreementTemplatesDocument = "/v1/agreementTemplates/{templateId}/document";
        public const string AgreementTemplatesDocumentWithParams = "/v1/agreementTemplates/{templateId}/document?language={language}&country={country}";
        public const string GetAgreements = "/v1/agreements";
        public const string GetAgreementsWithType = "/v1/agreements?agreementType=";
        public const string AuditActivityById = "/auditactivity/v1/auditrecords/{id}";
        public const string AuditActivityByStartDate = "/auditactivity/v1/auditrecords?auditRequest.startDate={auditRequest.startDate}";
        public const string AuditActivityByFilterField = "/auditactivity/v1/auditrecords?auditRequest.filter.field=";
        public const string GenerateToken = "/generatetoken";
        public const string UsageBudget = "/v1/customers/{customer_id}/usagebudget";
        public const string GetUsageRecords = "/v1/customers/usagerecords";
        public const string UsageRecordsBySubscription = "/v1/customers/{customer_id}/subscriptions/{subscription_id}/usagerecords/resources";
        public const string GetUsageSummaryByCustommer = "/v1/customers/{customer_id}/usagesummary";
        public const string MeterUsageRecordsBySubscription = "/v1/customers/{customer_id}/subscriptions/{subscription_id}/meterusagerecords";
        public const string GetUsageSummary = "/v1/usagesummary";
        public const string ResourceUsageRecords = "/v1/customers/{customer_id}/subscriptions/{subscription_id}/resourceusagerecords";
        public const string SubscriptionUsageRecords = "/v1/customers/{customer_id}/subscriptions/usagerecords";
        public const string SubscriptionUsageSummary = "/v1/customers/{customer_id}/subscriptions/{subscription_id}/usagesummary";
        public const string CustomerUsageBudget = "/v1/customers/{customer_id}/usagebudget";
        public const string CancelAzureEntitlement = "/v1/customers/{customer_id}/subscriptions/{subscription_id}/azureEntitlements/{entitlement_id}/cancel";
        public const string ProductUpgrades = "/v1/productUpgrades";
        public const string AzureEntitlements = "/v1/customers/{customer_id}/subscriptions/{subscription_id}/azureEntitlements";
        public const string AzureEntitlementById = "/v1/customers/{customer_id}/subscriptions/{subscription_id}/azureEntitlements/{entitlement_id}";
        public const string ProductUpgradesEligibility = "/v1/productUpgrades/eligibility";
        public const string ProductUpgradesById = "/v1/productUpgrades/{upgradeId}";
        public const string ProductUpgradesStatus = "/v1/productUpgrades/{upgradeId}/status";
        public const string ReactivateAzureEntitlement = "/v1/customers/{customer_id}/subscriptions/{subscription_id}/azureEntitlements/{entitlement_id}/reactivate";
        public const string CreateDeviceBatchById = "/v1/customers/{customer_id}/deviceBatches/{deviceBatch_id}/devices";
        public const string CustomerPolicies = "/v1/customers/{customer_id}/policies";
        public const string DeviceBatch = "/v1/customers/{customer_id}/deviceBatches/{deviceBatch_id}";
        public const string DeviceBatchDevicesById = "/v1/customers/{customer_id}/deviceBatches/{deviceBatch_id}/devices/{device_id}";
        public const string BatchJobStatus = "/v1/customers/{customer_id}/batchJobStatus/{batchUploadTracking_id}";
        public const string DeviceBatches = "/v1/customers/{customer_id}/deviceBatches";
        public const string DeviceBatchDevices = "/v1/customers/{customer_id}/deviceBatches/{deviceBatch_id}/devices";
        public const string DevicePolicyUpdates = "/v1/customers/{customer_id}/DevicePolicyUpdates";
        public const string DeviceBatchDevice = "/v1/customers/{customer_id}/deviceBatches/{deviceBatch_id}/devices/{device_id}";
        public const string CreateDeviceBatch = "/v1/customers/{customer_id}/deviceBatches";
        public const string FraudEvents = "/v1/fraudEvents";
        public const string FraudEventsByStatus = "/v1/fraudEvents?EventStatus=";
        public const string UpdateFraudEventStatus = "/v1/fraudEvents/subscription/{subscriptionId}/status";
        public const string CreateSandboxIndirectReseller = "/v1/sandboxIndirectReseller";
        // Add the remaining endpoints here
    }


    // Main Method 
    static void Main(string[] args) 
    { 
        string baseUrl = MicrosoftAPIEndpoints.BaseUrl;
        string azureAdLoginEndpoint = MicrosoftAPIEndpoints.AzureADLoginEndpoint;
        string getAgreementsEndpoint = MicrosoftAPIEndpoints.Endpoints.GetAgreements;
        
        // statement 
        // printing Hello World! 
        Console.WriteLine("Hello World!"); 
  
        // To prevents the screen from 
        // running and closing quickly 
        Console.ReadKey(); 
    } 
}


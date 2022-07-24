import azure.functions as func
import azure.durable_functions as df

def orchestrator_function(context: df.DurableOrchestrationContext):
    image_name = yield context.call_activity('DownloadImage')
    image_analysis_result = yield context.call_activity('AnalyzeImage', image_name)
    cosmos_id = yield context.call_activity('StoreAnalysisResult', image_analysis_result)
    result = [{'image_name': image_name}, {'cosmos_id': cosmos_id}]
    return result

main = df.Orchestrator.create(orchestrator_function)
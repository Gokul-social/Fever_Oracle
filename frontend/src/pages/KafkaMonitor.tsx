import { KafkaMonitor } from "@/components/KafkaMonitor";
import { RealtimeDataStream } from "@/components/RealtimeDataStream";
import { ModelPredictions } from "@/components/ModelPredictions";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Database, Activity, TrendingUp } from "lucide-react";

const KafkaMonitorPage = () => {
  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto p-4 sm:p-6 space-y-4 sm:space-y-6">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl sm:text-3xl font-bold text-foreground mb-2">
              Kafka & Model Monitoring
            </h1>
            <p className="text-sm sm:text-base text-muted-foreground">
              Real-time data pipeline monitoring and ML model predictions
            </p>
          </div>
        </div>

        {/* Overview Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-sm font-medium flex items-center gap-2">
                <Database className="h-4 w-4 text-primary" />
                Kafka Pipeline
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-xs text-muted-foreground">
                Monitor real-time message throughput and topic statistics
              </p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-sm font-medium flex items-center gap-2">
                <Activity className="h-4 w-4 text-green-500" />
                Data Stream
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-xs text-muted-foreground">
                View live messages flowing through Kafka topics
              </p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-sm font-medium flex items-center gap-2">
                <TrendingUp className="h-4 w-4 text-warning" />
                ML Predictions
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-xs text-muted-foreground">
                Run predictions using real-time Kafka data
              </p>
            </CardContent>
          </Card>
        </div>

        {/* Main Components */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 sm:gap-6">
          <div className="space-y-4 sm:space-y-6">
            <KafkaMonitor />
            <ModelPredictions />
          </div>
          <div>
            <RealtimeDataStream />
          </div>
        </div>

        {/* Information Card */}
        <Card>
          <CardHeader>
            <CardTitle>How It Works</CardTitle>
            <CardDescription>Understanding the Kafka pipeline and model integration</CardDescription>
          </CardHeader>
          <CardContent className="space-y-3 text-sm text-muted-foreground">
            <div>
              <strong className="text-foreground">1. Kafka Producer:</strong> Generates realistic healthcare data 
              (wastewater, pharmacy, patient vitals, alerts) and publishes to Kafka topics.
            </div>
            <div>
              <strong className="text-foreground">2. Kafka Consumer:</strong> Backend service consumes messages 
              from Kafka topics and processes them in real-time.
            </div>
            <div>
              <strong className="text-foreground">3. Model Predictions:</strong> ML model analyzes the latest 
              Kafka data to predict outbreak risk levels with confidence scores.
            </div>
            <div>
              <strong className="text-foreground">4. Real-time Updates:</strong> All components update automatically 
              to show the latest data and predictions.
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default KafkaMonitorPage;


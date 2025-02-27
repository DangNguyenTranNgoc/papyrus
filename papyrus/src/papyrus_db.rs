use chrono::{DateTime, Utc};
use std::collections::HashMap;

#[derive(Debug, Clone)]
pub struct Metric {
    pub id: u32,
    pub model_id: u32,
    pub metric_name: String,
    pub metric_value: f64,
    pub created_date: DateTime<Utc>,
}

pub struct PapyrusDB {
    metrics: HashMap<u32, Metric>,
    next_id: u32,
}

impl PapyrusDB {
    /// Create a new PapyrusDB instance
    pub fn new() -> PapyrusDB {
        PapyrusDB {
            metrics: HashMap::new(),
            next_id: 1,
        }
    }

    /// INSERT: add new metric record into the database
    /// 
    /// # Arguments
    ///
    /// * `model_id` - The ID of the model
    /// * `metric_name` - The name of the metric
    /// * `metric_value` - The value of the metric
    ///
    /// # Returns
    ///
    /// * `&Metric` - The newly created metric record
    pub fn insert(&mut self, model_id: u32, metric_name: String, metric_value: f64) -> &Metric {
        let metric = Metric {
            id: self.next_id,
            model_id,
            metric_name,
            metric_value,
            created_date: Utc::now(),
        };
        self.metrics.insert(self.next_id, metric);
        self.next_id += 1;
        self.metrics.get(&(self.next_id -1)).unwrap()
    }

    /// Read metric record from the database by ID
    /// 
    /// # Arguments
    /// 
    /// * `id` - The ID of the read metric
    /// 
    /// # Returns
    /// 
    /// * `Option<&Metric>` - The metric record if found, otherwise None
    pub fn read(&self, id: u32) -> Option<&Metric> {
        self.metrics.get(&id)
    }

    /// UPDATE: Update metric record in the database
    /// 
    /// # Arguments
    /// 
    /// * `id` - The ID of the metric to be updated
    /// * `new_value` - The new value of the metric
    ///
    /// # Returns
    ///
    /// * `Option<&Metric>` - The updated metric record if found, otherwise None
    pub fn update(&mut self, id: u32, new_value: f64) -> Option<&Metric> {
        if let Some(metric) = self.metrics.get_mut(&id) {
            metric.metric_value = new_value;
            metric.created_date = Utc::now();
            Some(metric)
        } else {
            None
        }
    }

    /// DELETE: Delete metric record from the database
    ///
    /// # Arguments
    ///
    /// * `id` - The ID of the metric to be deleted
    ///
    /// # Returns
    ///
    /// * `Option<Metric>` - The deleted metric record if found, otherwise None
    pub fn delete(&mut self, id:u32) -> Option<Metric> {
        self.metrics.remove(&id)
    }

}

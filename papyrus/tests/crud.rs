use papyrus::papyrus_db::PapyrusDB;

#[test]
fn test_insert() {
    let mut db = PapyrusDB::new();
    let metric = db.insert(1, "accuracy".to_string(), 0.95);
    assert_eq!(metric.id, 1);
    assert_eq!(metric.model_id, 1);
    assert_eq!(metric.metric_name, "accuracy");
    assert_eq!(metric.metric_value, 0.95);
}

#[test]
fn test_read() {
    let mut db = PapyrusDB::new();
    db.insert(2, "MRSE".to_string(), 0.85);
    let metric = db.read(1).unwrap();
    assert_eq!(metric.id, 1);
    assert_eq!(metric.model_id, 2);
    assert_eq!(metric.metric_name, "MRSE");
    assert_eq!(metric.metric_value, 0.85);
}

#[test]
fn test_update() {
    let mut db = PapyrusDB::new();
    db.insert(2, "RMSE".to_string(), 0.75);
    let metric = db.update(1, 0.65).unwrap();
    assert_eq!(metric.metric_value, 0.65);
}

#[test]
fn test_delete() {
    let mut db = PapyrusDB::new();
    db.insert(2, "RMSE".to_string(), 0.75);
    db.delete(1);
    let metric = db.read(1);
    assert_eq!(metric.is_none(), true);
}

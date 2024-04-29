db = db.getSiblingDB('reto')
db.createUser(
    {
        user: "reto",
        pwd: "Extrovert-Unbiased9-Oxidize-Recycler",
        roles: [
            {
                role: "readWrite",
                db: "reto"
            }
        ]
    }
);
db.createCollection('commits', { capped: false });
db.createCollection('pipelines', { capped: false });
db.createCollection('pullrequests', { capped: false });
db.createCollection('repositories', { capped: false });
db.commits.createIndex({id: 1}, {unique: true})
db.commits.createIndex({timestamp: 1})
db.pullrequests.createIndex({created_at:1})
db.pullrequests.createIndex({closed_at:1}, {sparse: true})
db.pullrequests.createIndex({
    event_source: 1,
    action: 1
})
db.pipelines.createIndex({
    finished_at:1
})
db.pipelines.createIndex({
    result: 1,
    event_source:1
})
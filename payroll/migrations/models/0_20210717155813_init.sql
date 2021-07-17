-- upgrade --
CREATE TABLE IF NOT EXISTS "employee" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON TABLE "employee" IS 'An extensible class to manage Employees';
CREATE TABLE IF NOT EXISTS "job_group" (
    "group" VARCHAR(1) NOT NULL  PRIMARY KEY,
    "hourly_rate" DECIMAL(7,2) NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON TABLE "job_group" IS 'JobGroup enum mapping the 2 existing job groups with the ability to extend';
CREATE TABLE IF NOT EXISTS "time_report" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "date" DATE NOT NULL,
    "hours_worked" DECIMAL(4,2) NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "employee_id_id" INT NOT NULL REFERENCES "employee" ("id") ON DELETE CASCADE,
    "job_group_id" VARCHAR(1) NOT NULL REFERENCES "job_group" ("group") ON DELETE CASCADE
);
COMMENT ON TABLE "time_report" IS 'Time Report class to contain parsed CSV info';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(20) NOT NULL,
    "content" JSONB NOT NULL
);

-- upgrade --
CREATE TABLE IF NOT EXISTS "time_report" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "modified_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "report_id" INT NOT NULL,
    "date" DATE NOT NULL,
    "hours_worked" DECIMAL(4,2) NOT NULL,
    "employee_id" INT NOT NULL,
    "job_group" VARCHAR(1) NOT NULL
);
COMMENT ON TABLE "time_report" IS 'Time Report class to contain parsed CSV info... pretty much a data dump';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(20) NOT NULL,
    "content" JSONB NOT NULL
);

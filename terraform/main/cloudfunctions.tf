resource "google_project_service" "cloudfunctions" {
  project = var.project
  service = "cloudfunctions.googleapis.com"
}

resource "google_service_account" "cloudfunctions" {
  project     = var.project
  account_id  = "svc-my-cloudfunction"
  description = "Service account for cloud functions"
}

resource "google_project_iam_member" "cloudfunctions" {
  for_each = toset(var.svc_cloudfunctions_roles)
  role     = each.key
  project  = var.project
  member   = "serviceAccount:${google_service_account.cloudfunctions.email}"
}

variable "svc_cloudfunctions_roles" {
  description = "IAM roles to bind on service account"
  type        = list(string)
  default = [
    # For example: "roles/storage.objectViewer"
  ]
}

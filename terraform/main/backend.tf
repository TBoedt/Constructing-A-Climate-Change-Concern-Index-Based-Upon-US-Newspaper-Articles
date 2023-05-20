
/******************************************
	Remote backend configuration
 *****************************************/

# setup of the backend gcs bucket that will keep the remote state

terraform {
  backend "gcs" {
    bucket = "active-chimera-382918_terraform"
    prefix = "terraform/state"
  }
}

resource "google_compute_firewall" "internal-only" {
  name    = "internal-only-firewall-ssh"
  network = "sample-network"

  allow {
    protocol = "tcp"
    ports    = ["8080"]
  }

  target_tags   = ["internal-only-firewall-ssh"]
  source_ranges = ["10.10.10.0/24"]
}

resource "google_compute_firewall" "seattle-office" {
  name    = "seattle-office-firewall-ssh"
  network = "sample-network"

  allow {
    protocol = "tcp"
    ports    = ["443"]
  }

  target_tags   = ["seattle-office-firewall-ssh"]
  source_ranges = ["72.172.213.172/32"]
}



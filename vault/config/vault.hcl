ui = true

listener "tcp" {
  address       = "0.0.0.0:8200"
  tls_cert_file = "/certs/meridian.local.pem"
  tls_key_file  = "/certs/meridian.local-key.pem"
}

storage "file" {
  path = "/vault/data"
}

api_addr     = "https://vault.meridian.local:8200"
cluster_addr = "https://vault.meridian.local:8201"

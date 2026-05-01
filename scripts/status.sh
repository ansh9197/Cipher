#!/bin/bash
# Quick status check for all CIPHER services
echo "================================================"
echo "CIPHER System Status"
echo "================================================"
echo ""
echo "Containers:"
docker ps --format "  {{.Names}}: {{.Status}}" | grep cipher

echo ""
echo "Health checks:"
for port in 8001 8002 8003 8004 8005; do
  result=$(curl -s --max-time 3 http://localhost:$port/health 2>/dev/null)
  echo "  :$port ${result:-FAILED}"
done

echo ""
echo "Frontend:   $(curl -s --max-time 3 http://localhost:3000 > /dev/null 2>&1 && echo OK || echo FAILED)"
echo "MLflow:     $(curl -s --max-time 3 http://localhost:5000 > /dev/null 2>&1 && echo OK || echo FAILED)"
echo "Prometheus: $(curl -s --max-time 3 http://localhost:9090/-/healthy 2>/dev/null && echo '' || echo FAILED)"
echo "Grafana:    $(curl -s --max-time 3 http://localhost:3001/api/health > /dev/null 2>&1 && echo OK || echo FAILED)"
echo ""
echo "Kubernetes:"
kubectl get pods -n cipher --no-headers 2>/dev/null | awk '{print "  "$1": "$3}' || echo "  kubectl not configured"
echo "================================================"

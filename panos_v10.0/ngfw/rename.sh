for x in *..skillet.yaml.skillet.yaml; do
    mv "$x" "${x%..skillet.yaml.skillet.yaml}.skillet.yaml"
done
def generate_recommendations(dna_sequence):
    recommendations = []

    if 'ATCG' in dna_sequence:
        recommendations.append("Tingkatkan asupan antioksidan karena gen Anda sensitif terhadap stres oksidatif.")
    if 'GATTACA' in dna_sequence:
        recommendations.append("Anda mungkin membutuhkan latihan kardio rutin 3x seminggu.")
    if 'CGTA' in dna_sequence:
        recommendations.append("Disarankan tidur cukup karena ada gen yang terkait kualitas tidur.")
    if not recommendations:
        recommendations.append("Tidak ada rekomendasi khusus berdasarkan DNA Anda saat ini.")

    return recommendations

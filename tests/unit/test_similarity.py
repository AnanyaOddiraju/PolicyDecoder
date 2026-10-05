from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer("all-MiniLM-L6-v2")

sentences = [
    "Cats are the fluffiest creatures",
    "Dogs are also very cute and adorable",
    "Rainforests are scary"]

embeddings = model.encode(sentences)
#similarity_ab = model.similarity(embeddings[0], embeddings[1])
#checking cosine similarity -> if vecors are pointing same/ almost same direction then similarity =1 else 0
print("length of embeddings:", len(embeddings))
similarity_ab = util.cos_sim(embeddings[0], embeddings[1]) 
similarity_bc= util.cos_sim(embeddings[1], embeddings[2])
similarity_ac= util.cos_sim(embeddings[0], embeddings[2])
print("embeddings 1:", embeddings[0][:5])
print("embeddings 2:", embeddings[1][:5])
print("embeddings 3:", embeddings[2][:5])
print("cat vs dogs similarirty", similarity_ab)
print("dogs vs rainforests similarirty", similarity_bc)
print("cat vs rainforests similarirty", similarity_ac)
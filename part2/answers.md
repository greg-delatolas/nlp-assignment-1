# Turorial answers

### Questions

1. The pmf for `('good', 'day')` clearly changed, as did the pmf for `('day', 'good')`. Why is that?

   The model was trained for ten SGD steps on the positive example `('good', 'day', 1)`. Each step updated both the `good` and `day` embeddings to increase their dot product, which raised the predicted co-occurrence probability from about 0.09 to 0.96. The reversed pair changed in exactly the same way because the dot product is symmetric:

   `embedding(good) · embedding(day) = embedding(day) · embedding(good)`

   Consequently, this model assigns the same PMF to both word orders.

2. Not only those two pmfs changed, but also other pmfs changed. Which and why did they change?

   Every displayed pair containing either `good` or `day` could change because those were the two embeddings updated during training:

   - `('good', 'bad')`: its positive probability changed slightly from about 0.03 to 0.04.
   - `('bad', 'day')`: its positive probability decreased from about 0.78 to 0.63.
   - `('day', 'another')`: its positive probability increased from about 0.57 to 0.86. 

   A pair's prediction depends on the dot product of its two embeddings, so changing one embedding changes its relationship with every other word vector. The probability may increase or decrease depending on the direction of the update. `('another', 'regular')` remained unchanged at about 0.93 because neither of its embeddings was updated.


3. Do you think an embedding space for English might contain information about, for example, parts of speech (i.e., syntactic word categories like _noun_, _verb_, _adjective_ and _adverb_)? Use your knowledge about how pretrained embeddings are typically trained to justify your answer.

   Yes. During training, the model learns from **target–context word pairs**.

   For example, from:

   > “The beautiful city attracts tourists.”

   The model may create pairs such as:

   ```scss
   (beautiful, city)
   (city, the)
   (city, attracts)
   (attracts, tourists)
   ```

   Other adjectives such as `large`, `modern`, and `old` also frequently occur before nouns. They therefore have similar training pairs and receive similar embeddings.

   The model is not explicitly told that a word is a noun, verb, or adjective. Part-of-speech information emerges because words with the same grammatical role tend to appear in similar contexts.

4. Do you think your answer might change depending on the _language_ of the corpus used for training? Again, use your knowledge about how pretrained embeddings are typically trained to justify your answer.

   Yes. Languages express grammatical information differently.

   English relies strongly on word order. For example:

   - “The dog bites the man.”
   - “The man bites the dog.”

   Changing the order changes the meaning and also changes the target–context pairs used during training.

   Other languages may use word endings or case markers to indicate grammatical roles, allowing more **flexible word order**. In those languages, embeddings may learn more grammatical information from word forms and less from word position.

5. Can you think of an alternative definition of co-ocurrence capable of having a decisive impact on the kind(s) of information pretained embeddings are likely to capture? Explain the rationale for your answer. For this question you can imagine access to additional levels of linguistic information to be available for the texts in your training corpus.

   Yes. Instead of defining co-occurrence as words appearing close together, we could define it using grammatical relationships.

   For example, in:

   > “The student reads a book.”

   A dependency-based model could create relationships such as:

   ```scss
   (student, subject-of-reads)
   (book, object-of-reads)
   ```

   Words such as `student`, `teacher`, and `child` may then receive similar embeddings because they often occur as subjects of similar verbs.

   Normal window-based co-occurrence often captures topics. For example, `doctor` and `hospital` may be similar because they frequently appear near each other. Dependency-based co-occurrence would capture more information about grammatical roles.


5. Reflect on your observations in exercises (1; cosine), (2; top-k) and (3; analogies). Can you explain what aspect of the model's training procedure might justify the observations you made?

   The model was trained using **target–context word pairs** from a large amount of text. Words that occur in similar contexts receive similar vectors.

   For example, `city` and `town` often occur near words such as `mayor`, `people`, and `centre`. Their vectors therefore become similar, which explains why `town` is one of the nearest words to `city`.

   The model also learns relationships as directions in the embedding space. For example:

   ```text
   king − man + woman ≈ queen
   ```

   However, it learns biases and unusual associations from the training text too. For example, changing the gender direction of `nurse` produces different profession-related words. `burger` appears near `king` because “Burger King” occurs frequently in text.

6. Accepting that a certain embedding space contains information that's coherent with human assessment of lexical similarity, why should _cosine_ between two vectors in this space, as opposed to some other way to map two vectors to a single real number,  happen to be useful? 

   Cosine similarity compares the **direction** of two vectors and mostly ignores their length. Words with similar contextual patterns usually point in similar directions.

   For example, suppose the training corpus contains sentences such as “The king ruled the country” and “The queen ruled the country.” If the context window is large enough, the model gathers target–context observations such as:

   ```text
   (king, ruled)
   (king, country)
   (queen, ruled)
   (queen, country)
   ```

   These are illustrative pairs: the exact pairs depend on the corpus and the chosen context-window size. Because `king` and `queen` repeatedly occur with similar context words, dot-product-based training moves their vectors toward similar directions. Cosine similarity detects this directional alignment.

   For another geometric example:

   ```ini
   u = [1, 2]
   v = [10, 20]
   ```

   These vectors have different lengths, but they point in the same direction. Their cosine similarity is therefore `1`.

   This is useful because vector length can be affected by factors such as word frequency. Cosine focuses more on the learned contextual pattern, which is why related words such as `computer` and `software` receive a high similarity.

# Get to work!

1. Find a word embedding model that is appropriate for your dataset. Think about the language, the kind of text you are working with. Find evidence that your choice is a good one: 
    * Can you tokenize your texts in a way coherent with the definition of a token in the embedding model?
    A: We tokenized using a word tokenizer, because the GloVe twitter is a word level embedding vector.
    * Does the model's vocabulary give enough coverage to the words in your texts? etc.
    A: Yes, check the analysis at project.ipynb
2. Explore what your chosen word embedding model captures. Some things you might consider: 
    * Is it good at representing interesting similarities (re to your choice of task)? J
    A: Analysis on GloVe twitter vs GloVe Wikipedia.
    * Have you found task-specific evidence that it's better than some other reasonable alternative?
    * Do you know about limitations of this model?
    * Any limitations that you find particularly troubling for your task? 
3. Experiment with the embed-and-pool approach.  
    * What design choices have meaningful impact in classification performance (eg, embedding size, architecture design, optimisation parameters), if any?
    * Is this better than what you could achieve last week? In other words, did pretrained embeddings add to your design?
4. Experiment with a recurrent encoder (GRU or LSTM). 
    * What design choices have meaningful impact in classification performance, if any?
    * Did you investigate the impact of data size, embedding parameters (trained or not, fixed or trainable, etc)?
    * Did you struggle with over-fitting?
    * How far can this approach go? Are you able to improve meaningfully on embed-and-pool?
5. We make decisions under uncertainty all the time, are you gathering enough information to substantiate your choices? Various things can lead to small differences in results, and these differences are not always consistent. Here are some things to think about:
    * How did you structure you hyperparameter search?
    * Are you keeping an eye on experimental variance?
6. Experiment with error analysis and try to discover what characteristics of input texts are predictive of performance differences across major design choices. 
    * What analysis features did you come up with?
    * Which ones did you manage to test and how did that go?
    * What would you prioritise in the future in order to improve your systems?

Be mindful that you will be using your experiments to write up your final blog, so make sure your code is clean and neat!

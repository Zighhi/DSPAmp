# Romanian Academic Writing & Anti-AI Strategy

This reference guide provides rules for writing formal technical documentation in Romanian that bypasses AI detection and maintains high academic standards.

## 1. Formal Tone (Academic Standard)
*   **Use the Reflexive Passive:** Use "Se observă că..." or "S-a implementat..." instead of "Am observat" or "Eu am implementat".
*   **Precision over Fluff:** Avoid adjectives like "foarte bun", "uimitor", "revoluționar". Use technical metrics instead (e.g., "SNR de 90dB", "latență sub 1ms").
*   **Connective Logic:** Use logical connectors like "Prin urmare", "Astfel", "În acest sens", but use them sparingly to avoid AI patterns.

## 2. Bypassing AI Detection
AI detectors often look for "evenness" in sentence length and high predictability in word choice. To bypass this:
*   **Vary Sentence Structure:** Mix short, punchy technical statements with longer, explanatory complex sentences.
*   **Use Specific Jargon:** Instead of "the chip handles sound," use "procesorul SigmaDSP efectuează manipularea semnalului în domeniul digital prin intermediul algoritmilor de filtrare biquad".
*   **Avoid "AI Tropes":**
    *   Never start every paragraph with "În plus" or "În concluzie".
    *   Avoid lists of three items unless necessary.
    *   Don't over-explain basic concepts (e.g., don't explain what a resistor is unless the specific value's derivation is the point).
*   **Integrate Local Context:** Mention specific file paths, component names (ADAU1701, OPA2134), and previous chapter references (e.g., "Conform proiectării detaliate în Capitolul 2...").

## 3. LaTeX Integration
*   **Citations:** Always check `referinte.bib` and use `\cite{key}`.
*   **References:** Use `\ref{fig:label}` for figures and `\ref{theory}` for chapters/sections.
*   **Math:** Use `\begin{equation}` for important formulas.
*   **Lists:** Use `\begin{itemize}` or `\begin{enumerate}` for requirements or objectives.

## 4. Common Romanian Academic Phrases
*   "Lucrarea de față propune..."
*   "Analiza efectuată relevă faptul că..."
*   "Sistemul a fost validat prin..."
*   "Configurația hardware include..."
*   "Rezultatele obținute demonstrează..."

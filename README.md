# Knowledge-Representation

## Project Description
this project implements a First-order Logic resolution program. That includes a Parser and Skolemization conversions, and Unification.

## Assignment Requirements
- Q1 & Q2: `FOL_SKOLEM.py`
- Q3: `MGU.py`
- Q4: `Resolution.py` and `Barber_issue.py`

## How to Run
- for question 1 and 2, `FOL_SKOLEM.py` would ask you to input a signature and theory, and check if the theory satisfy your signature, it will also transfer your theory to skolem formation.
- for question 3, `MGU.py` would ask you to input two predicates and check if it is unifiable.
- for question 4, `Resolution.py` will ask you to input a theory and check if it is valid or not, then run `Barber_issue.py` to resolute(fails).


## Project Structure
- `Token.py`: form a dict that help find matched token so that to find scope for function, relation and logical operators.
- `FOL_SKOLEM.py`: input a signature and theory, and check if the theory satisfy the signature, it will also transfer the theory to skolem formation.
- `MGU.py`: check two input predicates if they are unifiable.
- `Resolution.py`: resolute with one theory.

## Clarifications
- when define your relation and function, attention not to include any letter in "FORALL EXISTS"

## Assignment2
## Project Structure
- `NNF.py`: form a NNF for each ABox.
- `ALCQ_expand.py`: defines 7 expand rules
- `test.py`: reduce TBox, convert subsumption problem into NNF and prove given ABox whether consistent. I used third question and fouth question as a testset and prove those two subsumptions are valid with empty TBox, and joe ABox is consistent if those three child names represent the same individule. YOU CAN DIRECTLY RUN IT ON YOUR DATASET.
- `global.txt`: defines operaters when forming questions.

## Example
# Check consistency
ABox is ["H(joe, ann)", "H(joe, eva)", "H(joe, mary)", "P.T(joe)", "T(ann)", "T(eva)", "T(mary)", "T(joe)"], TBox is ["P≡<=2H"].
We want to check our ABox for consistency and find a corresponding model (if such exists). For this, we convert ABox in a way that is described in input format section:
`H(joe, ann)	H(joe, eva)	H(joe, mary)	P.T(joe)	T(ann)	T(eva)	T(mary)	T(joe)`
`P≡<=2H`
After that we run the reasoner with following command:
`python test.py ABox1.txt TBox1.txt`

# Checking subsumption
We want to check consistency of the following subsumption with respect to an empty TBox:
`∀r.∀s.A ⊓ ∃r.∀s.B ⊓ ∀r.∃s.C ⊑ ∃r.∃s.(A ⊓ B ⊓ C)`
we convert theory in a way that is described in input format section:
`ad(FORALL(r, FORALL(s, A)), EXISTS(r, FORALL(s, B)), FORALL(r, EXISTS(s, C))) BELONGto EXISTS(r, EXISTS(s, ad(A, B, C)))`
After that we run the reasoner with following command:
`python test.py theory1.txt`

We want to check consistency of the following subsumption with respect to an empty TBox:
`∀r.∀s.A ⊓ (∃r.∀s.¬A ⊔ ∀r.∃s.B) ⊑ ∀r.∃s.(A ⊓ B) ⊔ ∃r.∀s.¬B`
we convert theory in a way that is described in input format section:
`ad(FORALL(r, FORALL(s, A)), or(EXISTS(r, FORALL(s, not(A))), FORALL(r, EXISTS(s, B)))) BELONGto or(FORALL(r, EXISTS(s, ad(A, B))), EXISTS(r, FORALL(s, not(B))))`
After that we run the reasoner with following command:
`python test.py theory2.txt`

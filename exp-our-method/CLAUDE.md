# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a neural dependency parsing research project implementing a cross-domain parser with Mamba-based architectures. The codebase contains multiple experimental variants:
- `src-our-method/`: Main implementation with enhancement features
- `src-wo-enhance/`: Variant without enhancement
- `src-wo-filter/`: Variant without filtering

The parser uses a biaffine attention mechanism combined with Mamba (state space model) and transformer architectures for dependency parsing tasks, with domain adaptation capabilities for cross-lingual parsing (primarily Chinese-Vietnamese).

## Running the Code

### Training
```bash
cd src-our-method
bash run.sh
```

The `run.sh` script handles:
1. Dictionary creation (if needed): `--is_dictionary_exist 0 --is_train 1 --is_test 0`
2. Training: `--is_dictionary_exist 1 --is_train 1 --is_test 0`
3. Testing: `--is_train 0 --is_test 1 --model_eval_num <num>`

### Direct Python Execution
```bash
python main.py --exp_des <description> --config_file config.txt --random_seed <seed>
```

### Configuration
All hyperparameters are in `config.txt` using INI format with sections:
- `[Run]`: Runtime settings (device, paths, model flags)
- `[Train]`: Training data paths and training loop parameters
- `[Network]`: Model architecture dimensions and dropout ratios
- `[Optimizer]`: Learning rates, decay, clipping, loss weights

Key flags in config.txt:
- `is_use_mamba`: Enable Mamba layers (state space models)
- `is_use_lstm`: Enable LSTM layers
- `is_use_kan`: Enable KAN (Kolmogorov-Arnold Network) layers
- `is_meta`: Enable meta-learning
- `is_adversary`: Enable adversarial domain adaptation
- `is_charlstm`: Enable character-level LSTM

## Architecture

### Core Components

**Parser (`parser.py`)**: Main orchestrator that:
- Initializes vocabularies (words, tags, labels, characters)
- Builds the neural network stack (embedding → encoder → biaffine classifier)
- Manages training/evaluation loops with bucketing for efficient batching
- Handles domain adaptation with meta-learning and adversarial training

**Classifier (`classifier.py`)**: Implements biaffine attention for arc/label scoring:
- `BiaffineParser`: Main biaffine scoring mechanism for dependency arcs and labels
- `ClassificationD`/`ClassificationDnew`: Domain discriminators with gradient reversal layer (GRL)
- Uses orthogonal initialization for weight matrices

**Neural Modules (`nn_modules.py`)**: Building blocks including:
- `WeightNetwork`: Meta-learning weight generation for layer-wise adaptation
- `LossWeightNetwork`: Dynamic loss weighting across layers
- Biaffine layers with dropout

**Encoder Options**:
- `mambaformer.py`: Hybrid Mamba-Transformer architecture
- `models/MambaFormer.py`: Alternative MambaFormer with AM (Attention-Mamba) layers
- `CPMLSTM.py`: Character-level LSTM for subword representations
- `mymamba.py`: Custom Mamba block implementations

### Data Flow

1. **Input**: CoNLL-U format files (Universal Dependencies)
2. **Instance Creation** (`instance.py`): Parse CoNLL-U into structured instances with:
   - Word/tag/head/label sequences
   - Domain IDs for multi-domain training
   - Character-level representations
3. **Dataset** (`dataset.py`): Bucketing by sentence length for efficient batching
4. **Embedding**: Word embeddings + optional character LSTM + domain embeddings
5. **Encoding**: Mamba/LSTM/Transformer layers
6. **Scoring**: Biaffine attention for arc and label prediction
7. **Loss**: Cross-entropy + optional adversarial loss + meta-learning loss

### Domain Adaptation

The parser supports cross-domain/cross-lingual transfer:
- **Domain embeddings**: Learnable embeddings per domain
- **Adversarial training**: GRL-based domain discriminator to learn domain-invariant features
- **Meta-learning**: Layer-wise weight networks that adapt representations per domain
- **Differential loss weighting**: `is_diff_loss` enables dynamic loss balancing

## Key Files

- `main.py`: Entry point, sets random seeds and initializes Parser
- `config.py`: Configuration file parser (INI format)
- `vocab.py`: Vocabulary management (word/tag/label dictionaries)
- `optimizer.py`: Custom optimizer with learning rate scheduling
- `simple_bucketing.py`: Sentence length bucketing for batching
- `k_means.py`: K-means clustering for bucketing
- `bertembed.py`/`bertvocab.py`: BERT-based embeddings (optional)

## Data Format

Input files are CoNLL-U format with tab-separated columns:
```
ID  FORM  LEMMA  UPOS  XPOS  FEATS  HEAD  DEPREL  DEPS  MISC
```

The parser primarily uses: FORM (word), UPOS (POS tag), HEAD (dependency head), DEPREL (dependency relation).

## Model Outputs

- Trained models saved as `models-<eval_num>/` directories
- Logs: `log.train`, `log.test-<num>`, `log.create-dict`
- Dictionary files in `dict/`: words, chars, postags, labels

## Dependencies

- PyTorch with CUDA support
- `mamba_ssm`: Mamba state space model implementation
- Standard scientific Python: numpy, scipy
- Optional: transformers (for BERT embeddings)
- omegaconf, hydra-core: Configuration management

**Note on fairseq**: The project uses a local copy of fairseq modules (`fairseq_modules/`) instead of installing the full fairseq package. This includes:
- `utils.py`: Utility functions
- `incremental_decoding_utils.py`: Incremental decoding support
- `fairseq_dropout.py`: FairseqDropout module
- `quant_noise.py`: Quantization noise module

These modules are copied from fairseq source to avoid compatibility issues with Python 3.12+.

## Notes

- The codebase has hardcoded paths (e.g., `/home/ljj/mydata/`) that need adjustment for different environments
- GPU device is specified in config.txt: `device = cuda:0`
- Random seeds are set for reproducibility across numpy, torch, and torch.cuda
- Bucketing is used by default (`max_bucket_num = 80`) for efficient training with variable-length sentences

## Language Preference

- 用户偏好使用中文进行交流
- 在回复时优先使用中文，除非涉及代码、技术术语或英文文档引用

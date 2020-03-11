## NBC-Blockchain

Semester project for _**Distributed Systems**_ @ ECE NTUA

The purpose was to create a bitcoin-like blockchain (without merkle proofs etc) called NoobCoin (NBC)

The code is included in Scaffold_Code folder

This is a collaborate effort of the following contibutors:

| Name       | Surname | Semester |
| ----- | ------- | ------- |
| Panagiotis | Tzortzis | 9 |
| Dafne | Papaefthimiou | 9 |
| Danae | Xezonaki | 11 |

**DISCLAIMER**

Although this is a fully functional blockchain, it faces some problems due to its architecture. It has practical synchronization problems because of multiple threads accessing the same memory (see FLASK documentation for details). We made some efforts to counter these problems, but since the goal of this course was an introduction to Distributed Systems and not multi-thread programming, you may encounter some bugs if you stress the system with a lot of transactions.
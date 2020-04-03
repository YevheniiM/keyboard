import random
import torch
import torch.nn as nn
from torch import optim
import torch.nn.functional as F

import numpy as np


class EncoderRNN(nn.Module):
    def __init__(self, input_size, hidden_size, n_layers=1, dropout=0.1):
        super(EncoderRNN, self).__init__()
        
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.n_layers = n_layers
        self.dropout = dropout
        self.gru = nn.GRU(input_size, hidden_size, n_layers, dropout=self.dropout, bidirectional=True, batch_first=True)
        
    def forward(self, input_seqs, input_lengths, hidden=None):
        # Note: we run this all at once (over multiple batches of multiple sequences)
        packed = torch.nn.utils.rnn.pack_padded_sequence(input_seqs, input_lengths, batch_first=True)
        outputs, hidden = self.gru(packed, hidden)
        outputs, output_lengths = torch.nn.utils.rnn.pad_packed_sequence(outputs, batch_first=True) # unpack (back to padded)
        outputs = outputs[:, :, :self.hidden_size] + outputs[:, : ,self.hidden_size:] # Sum bidirectional outputs
        return outputs, hidden



class Attn(nn.Module):
    def __init__(self, method, hidden_size):
        super(Attn, self).__init__()
        
        self.method = method
        self.hidden_size = hidden_size
        
        if self.method == 'general':
            self.attn = nn.Linear(self.hidden_size, hidden_size)

        elif self.method == 'concat':
            self.attn = nn.Linear(self.hidden_size * 2, hidden_size)
            self.v = nn.Parameter(torch.FloatTensor(1, hidden_size))

    def forward(self, hidden, encoder_outputs):
        max_len = encoder_outputs.size(1)
        this_batch_size = encoder_outputs.size(0)

        # Create variable to store attention energies
        attn_energies = torch.zeros(this_batch_size, max_len) # B x S


        attn_energies = attn_energies.cuda()

        # For each batch of encoder outputs
        for b in range(this_batch_size):
            # Calculate energy for each encoder output
            for i in range(max_len):
                attn_energies[b, i] = self.score(hidden[b, :].squeeze(0), encoder_outputs[b, i])

        # Normalize energies to weights in range 0 to 1, resize to 1 x B x S
        return F.softmax(attn_energies).unsqueeze(1)
    
    def score(self, hidden, encoder_output):
        
        if self.method == 'dot':
            energy = hidden.dot(encoder_output)
            return energy
        
        elif self.method == 'general':
            energy = self.attn(encoder_output)
            energy = hidden.dot(energy)
            return energy
        
        elif self.method == 'concat':
            energy = self.attn(torch.cat((hidden, encoder_output), 1))
            energy = self.v.dot(energy)
            return energy


class LuongAttnDecoderRNN(nn.Module):
    def __init__(self, attn_model, input_size, hidden_size, output_size, n_layers=1, dropout=0.1):
        super(LuongAttnDecoderRNN, self).__init__()

        # Keep for reference
        self.input_size = input_size
        self.attn_model = attn_model
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.n_layers = n_layers
        self.dropout = dropout

        self.gru = nn.GRU(input_size, hidden_size, n_layers, dropout=dropout, batch_first=True)
        self.concat = nn.Linear(self.hidden_size * 2, self.hidden_size)
        self.out = nn.Linear(self.hidden_size, self.output_size)
        
        if attn_model != 'none':
            self.attn = Attn(attn_model, hidden_size)

    def forward(self, input_seq, last_hidden, encoder_outputs):

        rnn_output, hidden = self.gru(input_seq, last_hidden)

        attn_weights = self.attn(rnn_output, encoder_outputs)
        context = attn_weights.bmm(encoder_outputs) # B x S=1 x N

        # Attentional vector using the RNN hidden state and context vector
        # concatenated together (Luong eq. 5)
        rnn_output = rnn_output.squeeze(1) # S=1 x B x N -> B x N
        context = context.squeeze(1)       # B x S=1 x N -> B x N

        concat_input = torch.cat((rnn_output, context), 1)
        concat_output = F.tanh(self.concat(concat_input))

        # Finally predict next token (Luong eq. 6, without softmax)
        output = F.log_softmax(self.out(concat_output))

        # Return final output, hidden state, and attention weights (for visualization)
        return output, hidden, attn_weights


class AttentionAutoencoder(nn.Module):
    def __init__(self, dim, hidden_size, vs, n_layers, attn_model):
        super().__init__()
        self.encoder = EncoderRNN(dim, hidden_size, n_layers)
        self.decoder = LuongAttnDecoderRNN(attn_model, dim, hidden_size, vs, n_layers)
        
    def forward(self, hidden, lenX, X, leny, y):
        max_target_length = int(max(leny).item())
        decoder_input = y[:, :1]

        all_decoder_outputs = torch.zeros(X.size(0), max_target_length, self.decoder.output_size).cuda()


        # Run through decoder one time step at a time
        encoder_outputs, encoder_hidden = self.encoder(X, lenX, hidden)

        decoder_hidden = encoder_hidden[:self.decoder.n_layers]

        for t in range(max_target_length):

            decoder_output, decoder_hidden, decoder_attn = self.decoder(decoder_input, decoder_hidden, encoder_outputs)

            all_decoder_outputs[:, t] = decoder_output
            decoder_input = y[:, t+1].unsqueeze(1) # Next input is current target

        return all_decoder_outputs

if __name__ == '__main__':
    ds = AttentionAutoencoder(1003, 300, 2, 'general')
    print("here")

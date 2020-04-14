import torch

def loss(Y_hat, Y):
        # TRICK 3 ********************************
        # before we calculate the negative log likelihood, we need to mask out the activations
        # this means we don't want to take into account padded items in the output vector
        # simplest way to think about this is to flatten ALL sequences into a REALLY long sequence
        # and calculate the loss on that.

        # flatten all the labels
        Y = Y.view(-1).long()

        # flatten all predictions
        Y_hat = Y_hat.view(-1, Y_hat.size(-1))

        # create a mask by filtering out all tokens that ARE NOT the padding token
        tag_pad_token = 1000
        mask = (Y < tag_pad_token)

        # count how many tokens we have
        nb_tokens = int(torch.sum(mask).item())

        # pick the values for the label and zero out the rest with the mask
        Y_hat = Y_hat[:, Y] * mask

        # compute cross entropy loss which ignores all <PAD> tokens
        ce_loss = -torch.sum(Y_hat) / nb_tokens

        return ce_loss

def masked_ce_loss():
  return loss
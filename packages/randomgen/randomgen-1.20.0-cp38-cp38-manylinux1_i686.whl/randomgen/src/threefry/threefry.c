#include "threefry.h"

/* use_carry exists only for the old advance that resets buffer_pos after a call */
/* TODO: removed once the old method is deprecated */
#define _threefryNxW_advance_tpl(N, W)                                         \
void threefry##N##x##W##_advance(threefry_all_t *state, uint##W##_t *step, int use_carry) { \
  /* step has N+1 elements */                                                               \
  int i, next_buffer_pos;                                                                   \
  uint##W##_t last, carry, rem, adj_step;                                                   \
  threefry##N##x##W##_ctr_t ct;                                                             \
  rem = step[0] % N;                                                                        \
  next_buffer_pos = state->buffer_pos + rem;                                                \
  carry = (((state->buffer_pos == N) && (rem==0)) || (next_buffer_pos >= N && (rem > 0)))   \
            && (use_carry > 0);                                                             \
  state->buffer_pos = next_buffer_pos % N;                                                  \
  for (i = 0; i < N; i++) {                                                                 \
      adj_step = step[i] / N;                                                               \
      /* Add in the lower bits from the next step size */                                   \
      /* The N/2 is really log2(N) but ok here since N is 2 or 4  */                        \
      if (i < (N - 1)){                                                                     \
        adj_step += (step[i + 1] % N) << (W - (N / 2));                                     \
      }                                                                                     \
      last = state->state.state##N##x##W.ctr.v[i];                                          \
      state->state.state##N##x##W.ctr.v[i] += adj_step + carry;                             \
      carry = (last > state->state.state##N##x##W.ctr.v[i] ||                               \
               ((adj_step + carry)==0 && adj_step>0));                                      \
  }                                                                                         \
  /* Always regenerate the buffer at the current counter */                                 \
  ct = threefry##N##x##W(state->state.state##N##x##W.ctr, state->state.state##N##x##W.key); \
  for (i = 0; i < N; i++) {                                                                 \
	  state->buffer[i].u##W = ct.v[i];                                                      \
  }                                                                                         \
}

_threefryNxW_advance_tpl(2, 32)
_threefryNxW_advance_tpl(4, 32)
_threefryNxW_advance_tpl(2, 64)
_threefryNxW_advance_tpl(4, 64)

#define _threefryNxW_next_extern_tpl(N, W)                                            \
extern INLINE uint64_t threefry##N##x##W##_next64(threefry_all_t *state);    \
extern INLINE uint32_t threefry##N##x##W##_next32(threefry_all_t *state);    \
extern INLINE double threefry##N##x##W##_next_double(threefry_all_t *state);

_threefryNxW_next_extern_tpl(2, 32)
_threefryNxW_next_extern_tpl(4, 32)
_threefryNxW_next_extern_tpl(2, 64)
_threefryNxW_next_extern_tpl(4, 64)

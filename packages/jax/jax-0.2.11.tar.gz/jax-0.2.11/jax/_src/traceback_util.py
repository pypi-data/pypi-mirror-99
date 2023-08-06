# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys
import traceback
import types

from jax._src import util

_exclude_paths = [__file__, util.__file__]

def register_exclusion(path):
  _exclude_paths.append(path)

_jax_message_append = (
    'The stack trace above excludes JAX-internal frames.\n'
    'The following is the original exception that occurred, unmodified.\n'
    '\n--------------------')

def path_starts_with(path, path_prefix):
  path = os.path.abspath(path)
  path_prefix = os.path.abspath(path_prefix)
  if not os.path.exists(path_prefix):
    return False
  try:
    common = os.path.commonpath([path, path_prefix])
    return os.path.samefile(common, path_prefix)
  except ValueError:
    # path and path_prefix are both absolute, the only case will raise a
    # ValueError is different drives.
    # https://docs.python.org/3/library/os.path.html#os.path.commonpath
    return False

def include_frame(f):
  return not any(path_starts_with(f.f_code.co_filename, path)
                 for path in _exclude_paths)

# When scanning stack traces, we might encounter frames from cpython that are
# removed from printed stack traces, such as frames from parts of importlib. We
# ignore these frames heuristically based on source and name match.
def ignore_known_hidden_frame(f):
  return 'importlib._bootstrap' in f.f_code.co_filename

def filter_traceback_and_stack(e):
  out = None

  # Scan the traceback and collect relevant frames.

  for f, lineno in reversed(list(traceback.walk_tb(e.__traceback__))):
    if include_frame(f):
      out = types.TracebackType(out, f, f.f_lasti, lineno)  # pytype: disable=wrong-arg-count

  # Continue up the call stack.
  #
  # We would like to avoid stepping too far up, e.g. past the exec/eval point of
  # a REPL such as IPython. To that end, we stop past the first contiguous bunch
  # of module-level frames, if we reach any such frames at all. This is a
  # heuristic that might stop in advance of the REPL boundary. For example, if
  # the call stack includes module-level frames from the current module A, and
  # the current module A was imported from within a function F elsewhere, then
  # the stack trace we produce will be truncated at F's frame.

  reached_module_level = False
  for f, lineno in traceback.walk_stack(e.__traceback__.tb_frame):
    if ignore_known_hidden_frame(f):
      continue
    if reached_module_level and f.f_code.co_name != '<module>':
      break
    if include_frame(f):
      out = types.TracebackType(out, f, f.f_lasti, lineno)  # pytype: disable=wrong-arg-count
    if f.f_code.co_name == '<module>':
      reached_module_level = True

  return out

def is_reraiser_frame(f):
  return (f.filename == __file__ and
          f.name == 'reraise_with_filtered_traceback')

def is_under_reraiser(e):
  tb = traceback.extract_stack(e.__traceback__.tb_frame)
  return any(is_reraiser_frame(f) for f in tb[:-1])

def format_exception_only(e):
  return ''.join(traceback.format_exception_only(type(e), e)).strip()

def last_cause(e):
  prev, cur = e, e.__cause__
  while cur is not None:
    prev, cur = cur, cur.__cause__
  return prev

class FilteredStackTrace(Exception): pass

def filtered_tracebacks_supported():
  return sys.version_info >= (3, 7)

def api_boundary(fun):
  '''Wraps ``fun`` to form a boundary for filtering exception tracebacks.

  When an exception occurs below ``fun``, this appends to it a custom
  ``__cause__`` that carries a filtered traceback. The traceback imitates the
  stack trace of the original exception, but with JAX-internal frames removed.

  This boundary annotation works in composition with itself. The topmost frame
  corresponding to an ``api_boundary`` is the one below which stack traces are
  filtered. In other words, if ``api_boundary(f)`` calls ``api_boundary(g)``,
  directly or indirectly, the filtered stack trace provided is the same as if
  ``api_boundary(f)`` were to simply call ``g`` instead.

  This annotation is primarily useful in wrapping functions output by JAX's
  transformations. For example, consder ``g = jax.jit(f)``. When ``g`` is
  called, JAX's JIT compilation machinery is invoked, which in turn calls ``f``
  in order to trace and translate it. If the function ``f`` raises an exception,
  the stack unwinds through JAX's JIT internals up to the original call site of
  ``g``. Because the function returned by ``jax.jit`` is annotated as an
  ``api_boundary``, such an exception is accompanied by an additional traceback
  that excludes the frames specific to JAX's implementation.
  '''

  if not filtered_tracebacks_supported():
    return fun

  @util.wraps(fun)
  def reraise_with_filtered_traceback(*args, **kwargs):
    try:
      return fun(*args, **kwargs)
    except Exception as e:
      if not is_under_reraiser(e):
        filtered_tb, cause, filtered = None, None, None
        try:
          filtered_tb = filter_traceback_and_stack(e)
          if filtered_tb:
            msg = format_exception_only(e)
            msg = f'{msg}\n\n{_jax_message_append}'
            filtered = FilteredStackTrace(msg).with_traceback(filtered_tb)
            cause = last_cause(e)
            cause.__cause__ = filtered
            raise
          else:
            raise
        finally:
          del filtered_tb
          del cause
          del filtered
      else:
        raise
  return reraise_with_filtered_traceback

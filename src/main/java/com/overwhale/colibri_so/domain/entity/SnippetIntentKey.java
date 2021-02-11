package com.overwhale.colibri_so.domain.entity;

import lombok.Data;

import java.io.Serializable;
import java.util.UUID;

@Data
public class SnippetIntentKey implements Serializable {
  private UUID snippetId;
  private UUID intentId;
}

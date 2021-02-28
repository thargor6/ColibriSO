package com.overwhale.colibri_so.backend.entity;

import lombok.Data;

import java.io.Serializable;
import java.util.UUID;

@Data
public class UserAuthorityKey implements Serializable {
  private UUID userId;
  private UUID authorityId;
}
